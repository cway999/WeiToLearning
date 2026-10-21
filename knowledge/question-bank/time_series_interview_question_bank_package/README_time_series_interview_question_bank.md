# WeiToLearning — Time Series Interview Question Bank

The `.qmd` file is a **standalone Quarto website page**. It does not need an additional CSS or JS file, and it does not modify your site's `_quarto.yml`.

## Contents

| Topic tab | Questions |
|---|---:|
| Time Series Foundations & Diagnostics | 21 |
| Forecasting & Model Evaluation | 20 |
| ARIMA, SARIMA & Dynamic Regression | 21 |
| Econometrics: Cointegration & ECM | 23 |
| Machine Learning & Interview Cases | 23 |
| **Total** | **108** |

70 questions expand upon the source notes; 38 were added as complementary DS/Economist interview preparation. Every question has a concise **Reference Answer** and a longer **Detailed Explanation**. Three Python examples are embedded as *non-executing* fenced `python` blocks.

## Installation

1. Open your website project directory `WeiToLearning` in Finder or VS Code.
2. Copy `time_series_interview_question_bank.qmd` to `knowledge/question-bank/`.
3. Add a link on the home page (`index.qmd`), e.g.:

   ```markdown
   [Time Series Forecasting](knowledge/question-bank/time_series_interview_question_bank.qmd)
   ```

   If the link is written in `knowledge/index.qmd`, the correct relative path is:

   ```markdown
   [Time Series Forecasting](question-bank/time_series_interview_question_bank.qmd)
   ```

4. From the project root, run `quarto preview`.
5. Check that the five tabs appear and both toggles expand independently. Then run `quarto render` and publish via GitHub Desktop (`Commit` then `Push`).

The ZIP contains the `.qmd` in its intended `knowledge/question-bank/` folder, ready to merge into the project root, plus this README.

## Corrections made to the original notes

- ADF and KPSS have **different null hypotheses**; neither non-rejection is proof.
- Ljung–Box does **not** universally require `p > 0.1`.
- Annual seasonality of weekly data is approximately **52.18**, rather than exactly 52 observations.
- Dynamic regression does not require automatically differencing every nonstationary regressor; **cointegration** can justify certain levels relationships.
- ECM adjustment sign depends on the **definition of the error-correction gap** and on which variable adjusts.
- Realized future macro indicators create **ex-post** rather than ex-ante forecasts.
- Quarterly-to-monthly interpolation is **not** the observation of new data.
- Granger causality is **predictive precedence**, not the causal effect of intervening on a variable.
- Forecast errors and prediction intervals should be evaluated at genuine future cutoff dates, with **data publication lags and revisions** respected.

## Quality checks

- Markdown structure parsed with Pandoc, including 1 tabset, 108 Reference Answer callouts, and 108 Detailed Explanation callouts.
- All three Python examples were syntax-checked and executed with NumPy/statsmodels/scikit-learn. The KPSS diagnostic can legitimately warn about a test statistic outside a tabulated p-value range; the answer explains this.
- **Full Quarto rendering was not run in this environment**, so verify final styling in `quarto preview` on your Mac.

## External reading (additions beyond the source)

- [Forecasting: Principles and Practice, 3rd ed.](https://otexts.com/fpp3/)
- [statsmodels Time Series Analysis](https://www.statsmodels.org/stable/tsa.html)
- [scikit-learn lagged features & time-aware evaluation](https://scikit-learn.org/stable/auto_examples/applications/plot_time_series_lagged_features.html)
