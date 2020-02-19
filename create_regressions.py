
import numpy as np
import pandas as pd
import statsmodels.api as sm

def compute_regressions(measures_file, survey_file):

	measures_df = pd.read_csv(measures_file)
	measures_df['users'] = measures_df['users'].astype(str)

	survey_df = pd.read_csv(survey_file)
	survey_df = survey_df.drop(['7'], axis=1)
	survey_df['users'] = survey_df['users'].astype(str)

	true_users = []
	for user in survey_df['users'].values:
		if user in measures_df['users'].values and user in survey_df['users'].values:
			true_users.append(user)

	survey_df = survey_df[survey_df['users'].isin(true_users)].reset_index(drop=True)
	measures_df = measures_df[measures_df['users'].isin(true_users)].reset_index(drop=True)

	for col in survey_df.columns:
		if col == 'users': continue
		print(col)
		f = open(f'data/res{col}.csv', 'w+')
		xs = measures_df.set_index('users').astype(float).fillna(0)
		xs = sm.add_constant(xs)
		xs = xs[xs.columns]

		ys = survey_df[['users', col]].set_index('users').astype(float).fillna(0)
		ys = ys[col]

		combined = pd.concat([xs, ys], axis=1, sort=True)

		model = sm.OLS(combined[col], combined[combined.columns[:19]])
		result = model.fit()

		f.write(result.summary().as_csv())

		std = model.exog.std(0)
		std[0] = 1

		tt = result.t_test(np.diag(std))
		f.write(tt.summary().as_csv())

		f.close()

# modify to be your files.
compute_regressions('measure_outputs.csv', 'labeled_survey_answers.csv')
