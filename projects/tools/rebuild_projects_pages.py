from __future__ import annotations
from pathlib import Path
import html, re, json, shutil, zipfile, textwrap, subprocess
from bs4 import BeautifulSoup
from nbconvert import HTMLExporter
import nbformat

# Standalone builder, also copied into projects/tools so users can rebuild after editing notebooks.
CATEGORY = [
    ('ml','Machine Learning','Regression, feature engineering, search and ranking.', ['01','02']),
    ('dl','Deep Learning','Manual backpropagation and neural retrieval.', ['03','04']),
    ('transformers','Transformers','Search query correction and content-based recommendation.', ['05','06']),
    ('llm','LLM & AI Systems','Autoregressive generation and evidence-grounded retrieval.', ['07','08']),
    ('experiments','Experimentation','A/B analysis, metrics, logging failures and decisions.', ['09','10']),
    ('causal','Causal Inference','Policy evaluation, matching and Double Machine Learning.', ['11','12']),
]
INFO={
 '01':('Housing Prices & Mortgage Delinquency','Regression · Classification · Cross-validation','Build linear/logistic models and compare against stronger tabular baselines.'),
 '02':('E-commerce Search & Learning to Rank','BM25 · Pairwise Ranking · NDCG@10','Simulate queries and products, then improve relevance from lexical retrieval to learned ranking.'),
 '03':('Neural Network for Mortgage Delinquency','NumPy MLP · Backpropagation · PR-AUC','Derive gradients manually and benchmark against logistic regression.'),
 '04':('Two-Tower Neural Retrieval','Embeddings · Contrastive Loss · Recall@K','Train separate query and document towers for fast candidate retrieval.'),
 '05':('Transformer Search Query Correction','Encoder–Decoder · Attention · Exact Match','Build a tiny encoder–decoder for typo correction on synthetic search terms.'),
 '06':('Content-Based News Recommendation','TF-IDF · Transformer Encoder · Top-K','Compare a lexical baseline and a small neural text encoder.'),
 '07':('Tiny GPT: Product Description Generation','Decoder-only GPT · Causal Attention · Perplexity','Train an autoregressive Transformer on synthetic product descriptions.'),
 '08':('Mortgage Knowledge Retrieval & Grounded Answers','BM25 · Hybrid Retrieval · Citations','Evaluate retrieval and extractive answers; generative LLM integration is an extension.'),
 '09':('A/B Testing: Checkout Conversion','Randomization · Confidence Intervals · CUPED','Analyze simulated online experiments and make an evidence-based product decision.'),
 '10':('Advanced A/B: Search Ranking Metrics','SRM · Ratio Metrics · Bootstrap','Diagnose conflicting CTR and revenue metrics plus logging failures.'),
 '11':('DiD: First-Time Homebuyer Assistance','Panel Data · TWFE · Event Study','Estimate the impact of a simulated housing policy under identification assumptions.'),
 '12':('PSM vs Double ML: Mortgage Counseling','Matching · DML-IRM · ATT','Compare propensity-score matching with cross-fitted Double ML on the same target.'),
}

CSS=r'''
/* Scoped styles for both /projects/ and its 12 independent project subpages. */
#wtp{box-sizing:border-box;width:100%;max-width:1280px;min-width:0;margin:0 auto;padding:27px 28px 56px;--accent:#147f73;--primary:var(--bs-body-color,#273747);--muted:var(--bs-secondary-color,#6e7e88);--border:var(--bs-border-color,#dce6e9);--surface:var(--bs-body-bg,#fff);color:var(--primary);font-family:inherit;font-size:16px;line-height:1.65}
#wtp *{box-sizing:border-box}
#wtp [hidden]{display:none!important}
#wtp .hero{padding:6px 2px 23px;border-bottom:1px solid var(--border)}
#wtp .eyebrow{color:var(--accent);font-size:12px;font-weight:800;letter-spacing:.12em}
#wtp .hero h1{font-size:clamp(30px,2.8vw,36px);letter-spacing:-.034em;line-height:1.18;margin:7px 0 11px}
#wtp .lead{color:var(--muted);font-size:16px;line-height:1.7;max-width:860px;margin:0}
#wtp .stats{display:flex;flex-wrap:wrap;gap:19px;margin-top:15px;color:var(--muted);font-size:14px}
#wtp .stats strong{color:var(--primary)}
#wtp .layout{display:grid;grid-template-columns:228px minmax(0,1fr);gap:27px;width:100%;min-width:0;margin-top:24px;align-items:start}
#wtp .layout > *,#wtp .mainpane{min-width:0;max-width:100%}
#wtp .sidebar{grid-column:1;position:sticky;top:78px;border:1px solid var(--border);border-radius:12px;background:var(--surface);padding:13px 12px 15px;z-index:2}
#wtp .side-label{color:var(--muted);font-size:12px;font-weight:800;letter-spacing:.11em;padding:7px 10px 10px}
#wtp .side-list{display:flex;flex-direction:column;gap:3px}
#wtp .side-cat{color:var(--primary);border:0;border-radius:8px;text-decoration:none!important;font-size:15px;padding:10px;display:flex;justify-content:space-between;align-items:center;gap:8px;font-weight:500;cursor:pointer;line-height:1.4}
#wtp .side-cat:hover{background:rgba(20,127,115,.06);color:var(--accent)}
#wtp .side-cat[aria-current="page"]{background:rgba(20,127,115,.12);color:var(--accent);font-weight:750}
#wtp .side-count{font-size:12px;background:var(--surface);border:1px solid var(--border);border-radius:999px;padding:1px 7px;font-variant-numeric:tabular-nums}
#wtp .sidebar-hint{color:var(--muted);font-size:13px;padding:10px 10px 0;margin:0;line-height:1.6}
#wtp .mainpane{grid-column:2}
#wtp .panel-header{display:flex;align-items:end;justify-content:space-between;gap:13px;margin:2px 0 19px}
#wtp .panel-header h2{font-size:24px;letter-spacing:-.03em;margin:4px 0 6px;line-height:1.26}
#wtp .panel-header p{color:var(--muted);font-size:15px;margin:0}
#wtp .project-count{font-size:13px;white-space:nowrap;color:var(--muted);padding-bottom:5px}
#wtp .project-list{display:flex;flex-direction:column;gap:13px}
#wtp .project-card{border:1px solid var(--border);background:var(--surface);border-radius:12px;padding:19px 21px;min-width:0;transition:border-color .15s,box-shadow .15s}
#wtp .project-card:hover{border-color:rgba(20,127,115,.6);box-shadow:0 4px 18px rgba(20,127,115,.07)}
#wtp .number{color:var(--accent);font-weight:800;letter-spacing:.12em;font-size:12px}
#wtp .card-link{display:flex;align-items:center;justify-content:space-between;gap:12px;color:var(--primary);font-size:19px;font-weight:760;line-height:1.4;text-decoration:none!important;margin:6px 0}
#wtp .card-link:hover{color:var(--accent)}
#wtp .card-link .arrow{color:var(--accent);font-weight:600;font-size:17px}
#wtp .card-desc{font-size:15px;color:var(--muted);margin:6px 0 5px}
#wtp .tags{color:var(--accent);font-size:13px;font-weight:650}
#wtp .note{margin-top:22px;border-left:3px solid var(--accent);background:rgba(20,127,115,.05);border-radius:5px;font-size:14px;color:var(--muted);padding:12px 15px}
#wtp .back-link{color:var(--accent);font-size:14px;font-weight:700;text-decoration:none!important;display:inline-flex;align-items:center;gap:5px;margin-bottom:15px}
#wtp .back-link:hover{text-decoration:underline!important}
#wtp .project-title{font-size:clamp(28px,2.6vw,34px);margin:7px 0 8px;letter-spacing:-.03em;line-height:1.25}
#wtp .project-subhead{color:var(--muted);font-size:15px;margin:0 0 12px}
#wtp .detail-tools{display:flex;gap:10px 14px;align-items:center;flex-wrap:wrap;border:1px solid var(--border);border-radius:9px;padding:12px 15px;margin:16px 0 19px;font-size:14px}
#wtp .detail-tools a{color:var(--accent);font-weight:700;text-decoration:none!important}
#wtp .detail-tools a:hover{text-decoration:underline!important}
#wtp .detail-tools .label{color:var(--muted);margin-right:auto}
#wtp .code-action{border:1px solid var(--border);border-radius:6px;background:transparent;color:var(--accent);padding:5px 9px;cursor:pointer;font-size:13px;font-weight:650}
#wtp .nb-container{min-width:0;max-width:100%;overflow-wrap:anywhere}
#wtp .nb-container .text_cell{margin:0}
#wtp .nb-container .text_cell_render{font-size:16px;line-height:1.72}
#wtp .nb-container .text_cell_render h1{font-size:28px;letter-spacing:-.025em;line-height:1.25;margin:10px 0 12px}
#wtp .nb-container .text_cell_render h2{font-size:24px;margin:25px 0 9px;border-bottom:1px solid var(--border);padding-bottom:6px}
#wtp .nb-container .text_cell_render h3{font-size:20px;margin:17px 0 8px}
#wtp .nb-container .text_cell_render p{margin:9px 0}
#wtp .nb-container .text_cell_render blockquote{border-left:3px solid var(--accent);padding:8px 13px;margin:12px 0;background:rgba(20,127,115,.05)}
#wtp .nb-container .code_cell{margin:15px 0 20px}
#wtp .code-block{border:1px solid var(--border);border-radius:8px;overflow:hidden;margin:3px 0 10px}
#wtp .code-block summary{color:var(--accent);font-size:14px;font-weight:750;cursor:pointer;padding:9px 13px;background:rgba(20,127,115,.045)}
#wtp .code-block .input{margin:0}
#wtp .nb-container .input_area pre{font-size:13px;line-height:1.6;padding:13px;overflow-x:auto;white-space:pre;margin:0;background:var(--bs-tertiary-bg,#f6f8fa);border:0}
#wtp .nb-container pre{font-size:13px;line-height:1.6;overflow-x:auto;white-space:pre-wrap;word-break:break-word;max-width:100%}
#wtp .nb-container .output_wrapper{margin:7px 0 16px;max-width:100%}
#wtp .nb-container .output_subarea{max-width:100%;overflow-x:auto}
#wtp .nb-container .output_stream pre{background:var(--bs-tertiary-bg,#f6f8fa);border:1px solid var(--border);border-radius:6px;padding:12px}
#wtp .nb-container img{max-width:100%;height:auto;display:block;margin:10px auto}
#wtp .nb-container table{display:block;max-width:100%;overflow-x:auto;border-collapse:collapse;font-size:14px}
#wtp .nb-container th,#wtp .nb-container td{border:1px solid var(--border);padding:6px 9px;text-align:left}
#wtp .nb-container th{background:rgba(20,127,115,.05)}
#wtp .highlight .k,#wtp .highlight .kn{color:#0c6eac;font-weight:600}
#wtp .highlight .s,#wtp .highlight .s1,#wtp .highlight .s2{color:#a06b1a}
#wtp .highlight .c1{color:#768a97;font-style:italic}
#wtp .highlight .nf,#wtp .highlight .nb{color:#8054b6}
@media(max-width:850px){#wtp{padding:20px 18px 40px}#wtp .layout{grid-template-columns:184px minmax(0,1fr);gap:16px}#wtp .sidebar{padding:10px}#wtp .project-card{padding:15px}}
@media(max-width:650px){#wtp{padding:17px 12px 30px}#wtp .layout{grid-template-columns:1fr;gap:16px}#wtp .sidebar,#wtp .mainpane{grid-column:1}#wtp .sidebar{position:sticky;top:50px;padding:8px 9px;max-height:175px;overflow-y:auto}#wtp .side-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:4px}#wtp .side-cat{font-size:11px;padding:7px}#wtp .sidebar-hint,#wtp .side-label{display:none}#wtp .panel-header h2{font-size:24px}#wtp .detail-tools .label{width:100%}}
'''

INDEX_JS=r'''(function(){
  const root=document.getElementById('wtp'); if(!root)return;
  const names=new Set(['ml','dl','transformers','llm','experiments','causal']);
  function selected(){const param=new URLSearchParams(window.location.search).get('category');return names.has(param)?param:'ml';}
  function display(key,update){
    root.querySelectorAll('[data-category]').forEach(link=>{
      const active=link.dataset.category===key;
      if(active){link.setAttribute('aria-current','page');}else{link.removeAttribute('aria-current');}
    });
    root.querySelectorAll('.category-panel').forEach(p=>{p.hidden=p.dataset.panel!==key;});
    if(update){const url=new URL(window.location.href);url.searchParams.set('category',key);history.pushState({category:key},'',url);}
  }
  root.querySelectorAll('[data-category]').forEach(link=>link.addEventListener('click',e=>{
     e.preventDefault();display(link.dataset.category,true);
  }));
  window.addEventListener('popstate',()=>display(selected(),false));
  display(selected(),false);
})();'''
DETAIL_JS=r'''(function(){
  const root=document.getElementById('wtp');if(!root)return;
  const button=root.querySelector('#wtp-toggle-code');
  if(button){button.addEventListener('click',()=>{
    const blocks=Array.from(root.querySelectorAll('details.code-block'));
    const shouldOpen=blocks.some(el=>!el.open);
    blocks.forEach(el=>{el.open=shouldOpen;});
    button.textContent=shouldOpen?'Collapse code':'Expand code';
  });}
})();'''


def side_markup(active, depth):
    prefix='./' if depth==0 else '../'
    links=[]
    for key,title,desc,ids in CATEGORY:
        attrs=f' aria-current="page"' if key==active else ''
        links.append(f'<a class="side-cat" data-category="{key}" href="{prefix}?category={key}"{attrs}><span>{html.escape(title)}</span><span class="side-count">2</span></a>')
    return f'<div class="sidebar"><div class="side-label">BROWSE BY CATEGORY</div><nav aria-label="Project categories" class="side-list">{"".join(links)}</nav><p class="sidebar-hint">Choose a category to see its two projects. All notebooks open on separate pages.</p></div>'


def frontmatter(title, resource=None):
    resources=('resources:\n  - "index.ipynb"\n' if resource else '')
    return f'''---
title: "{title.replace('"', "'")} | WeiToLearning"
format:
  html:
    page-layout: custom
    toc: false
{resources}---
'''


def html_block(body, js):
    return '\n```{=html}\n<style>\n'+CSS+'\n</style>\n'+body+'\n<script>\n'+js+'\n</script>\n```\n'


def notebook_body(path):
    nb=nbformat.read(path,as_version=4)
    exporter=HTMLExporter(template_name='basic',exclude_input_prompt=True,exclude_output_prompt=True)
    output,_=exporter.from_notebook_node(nb)
    soup=BeautifulSoup(output,'html.parser')
    # The page itself already displays the project title. Remove the duplicate
    # first notebook H1 and nbconvert's visible pilcrow anchor links.
    for link in soup.select('a.anchor-link'):
        link.decompose()
    first_h1=soup.select_one('.text_cell_render h1')
    if first_h1 and first_h1.get_text(' ',strip=True).lower().startswith('project '):
        first_h1.decompose()
    code_nodes=soup.select('div.code_cell')
    for i,cell in enumerate(code_nodes,1):
        input_div=cell.select_one('div.input')
        if input_div:
            details=soup.new_tag('details',attrs={'class':'code-block'})
            if i<=2:details['open']=''
            summary=soup.new_tag('summary');summary.string=f'Python source · Cell {i}'
            details.append(summary)
            input_div.wrap(details)
    body=''.join(str(x) for x in soup.contents)
    assert '<script' not in body.lower(), path
    return body,len(code_nodes),body.count('data:image/png;base64')


def main(root=None, create_previews=True):
    if root is None: root=Path(__file__).resolve().parents[2]/'projects'
    root=Path(root).resolve()
    files={p.parent.name[:2]:p for p in sorted(root.glob('*/index.ipynb'))}
    assert sorted(files)==sorted(INFO),f'Expected all 12 notebooks in projects/; found {list(files)}'
    cat_by_pid={pid:key for key,_,_,ids in CATEGORY for pid in ids}
    sections=[]
    for key,title,desc,ids in CATEGORY:
        items=[]
        for pid in ids:
            name,tags,description=INFO[pid]
            slug=files[pid].parent.name
            items.append(f'''<article class="project-card"><div class="number">PROJECT {pid}</div>
              <a class="card-link" href="./{slug}/project.html"><span>{html.escape(name)}</span><span class="arrow">↗</span></a>
              <p class="card-desc">{html.escape(description)}</p><div class="tags">{html.escape(tags)}</div></article>''')
        sections.append(f'''<section class="category-panel" data-panel="{key}" {'hidden' if key!='ml' else ''}>
           <header class="panel-header"><div><span class="eyebrow">LEARNING TRACK</span><h2>{html.escape(title)}</h2><p>{html.escape(desc)}</p></div><span class="project-count">2 projects</span></header>
           <div class="project-list">{''.join(items)}</div></section>''')
    index_body=f'''<div id="wtp">
      <header class="hero"><div class="eyebrow">WEITOLEARNING / LEARN BY BUILDING</div><h1>Machine Learning & AI Projects</h1>
      <p class="lead">Twelve fully worked Jupyter notebooks. Select a learning track on the left, then open a dedicated project page for complete explanations, executable Python and saved charts.</p>
      <div class="stats"><span><strong>12</strong> projects</span><span><strong>6</strong> learning tracks</span><span><strong>Python · Jupyter · Quarto</strong></span></div></header>
      <div class="layout">{side_markup('ml',0)}<div class="mainpane">{''.join(sections)}
      <div class="note">All datasets are synthetic and educational. Open a project to see code and precomputed results. The source notebooks live in the same GitHub repository.</div></div></div>
    </div>'''
    idx=frontmatter('Projects')+html_block(index_body,INDEX_JS)
    (root/'index.qmd').write_text(idx,encoding='utf-8')
    reports=[]; detail_previews={}
    for pid,nbpath in files.items():
        key=cat_by_pid[pid];label=next(title for k,title,_,_ in CATEGORY if k==key)
        name,tags,description=INFO[pid]
        slug=nbpath.parent.name
        body,codes,plots=notebook_body(nbpath)
        github=f'https://github.com/cway999/WeiToLearning/blob/main/projects/{slug}/index.ipynb'
        detail=f'''<div id="wtp" data-project="{pid}">
         <header class="hero"><div class="eyebrow">WEITOLEARNING / LEARN BY BUILDING</div><h1>Machine Learning &amp; AI Projects</h1>
         <p class="lead">Twelve hands-on notebooks covering foundational ML, deep learning, transformers, experiments and causal inference.</p></header>
         <div class="layout">{side_markup(key,1)}<main class="mainpane" id="wtp-notebook-main">
         <a class="back-link" href="../?category={key}">← Back to {html.escape(label)} projects</a>
         <div class="number">PROJECT {pid} / 12</div>
         <h2 class="project-title">{html.escape(name)}</h2>
         <p class="project-subhead">{html.escape(tags)}</p>
         <div class="detail-tools"><span class="label">Executed notebook · Read-only website version</span>
         <a href="{github}" target="_blank" rel="noopener noreferrer">View on GitHub ↗</a>
         <a href="index.ipynb" download>Download Notebook ↓</a>
         <button class="code-action" id="wtp-toggle-code" type="button">Expand code</button></div>
         <div class="nb-container">{body}</div>
         <div class="note">Results shown here come from the saved notebook. To modify and rerun models, open the .ipynb in Jupyter or VS Code. This is a static website, not a live Python kernel.</div>
         <a class="back-link" href="../?category={key}" style="margin-top:22px">← All {html.escape(label)} projects</a>
         </main></div></div>'''
        qmd=frontmatter(name,resource=True)+html_block(detail,DETAIL_JS)
        out=nbpath.parent/'project.qmd'
        out.write_text(qmd,encoding='utf-8')
        detail_previews[pid]=detail
        reports.append(dict(project=pid,category=key,filename=slug+'/project.qmd',nb_bytes=nbpath.stat().st_size,html_bytes=out.stat().st_size,code_cells=codes,embedded_png=plots))
    (root/'SUBPAGE_BUILD_REPORT.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
    if create_previews:
        # HTML previews are stored outside projects/; do not accidentally publish them as site resources.
        previews=root.parent/'_projects_subpage_preview'
        previews.mkdir(parents=True,exist_ok=True)
        def as_html(body,js):
            sitebar='<header class="demo-bar"><b>Wei to Learning</b><span>Home</span><span>Technical Blog</span><span class="active">Projects</span><span>About</span></header>'
            return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>WeiToLearning Projects Preview</title><style>body{margin:0;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:#fff;color:#303a44}.demo-bar{height:55px;border-bottom:1px solid #e4e9eb;display:flex;align-items:center;gap:22px;padding:0 23px;font-size:13px}.demo-bar .active{color:#147f73}@media(max-width:480px){.demo-bar{padding:0 10px;gap:8px;font-size:11px}}</style><style>'+CSS+'</style></head><body>'+sitebar+body+'<script>'+js+'</script></body></html>'
        (previews/'index.html').write_text(as_html(index_body,INDEX_JS),encoding='utf8')
        for pid,detail in detail_previews.items():
            slug=files[pid].parent.name
            (previews/slug).mkdir(exist_ok=True)
            (previews/slug/'project.html').write_text(as_html(detail,DETAIL_JS),encoding='utf8')
            # Provide notebook download link for standalone previews.
            shutil.copy2(files[pid],previews/slug/'index.ipynb')
    return reports

if __name__=='__main__':
    base=Path(__file__).resolve().parents[2]/'projects'
    result=main(base)
    print('Generated category listing and',len(result),'standalone project pages.')
    for r in result:print(r['project'],r['category'],r['code_cells'],'code cells,',r['embedded_png'],'saved plots')
