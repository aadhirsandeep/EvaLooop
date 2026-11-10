| model | configuration | T | pass@1 | ASL_pow | ASL_bias | pass_drop | pass@10 | lang-compliant | summaries w/ code | truncated calls | API errors |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-3.5-flash | standard-mbpp-plus | 100 | 0.800 | 7.746 | 9.683 | 0.030 | 77 | - | 0/780 | 0 | 6 |
| gemini-3.5-flash | crosslingual-zh | 100 | 0.800 | 8.000 | 10.000 | 0.000 | 80 | 773/800 | 0/800 | 0 | 5 |
| gemini-3.1-flash-lite | standard-mbpp-plus | 100 | 0.770 | 7.013 | 9.108 | 0.070 | 70 | - | 0/709 | 0 | 161 |
| gemini-3.1-flash-lite | crosslingual-zh | 100 | 0.770 | 7.277 | 9.451 | 0.050 | 72 | 725/735 | 0/735 | 0 | 178 |

| model | extension | ΔASL_pow | 95% CI | shorter | longer | equal | cycle-1 pass agreement | broken (10→<10) | rescued (<10→10) |
|---|---|---|---|---|---|---|---|---|---|
| gemini-3.5-flash | crosslingual-zh | +0.254 | [+0.000, +0.580] | 0 | 3 | 97 | 100/100 | 0 | 3 |
| gemini-3.1-flash-lite | crosslingual-zh | +0.264 | [-0.135, +0.717] | 2 | 7 | 91 | 100/100 | 2 | 4 |
