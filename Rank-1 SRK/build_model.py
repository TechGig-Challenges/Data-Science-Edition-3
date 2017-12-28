import sys
import random
import operator
import pandas as pd
import numpy as np
import xgboost as xgb
import lightgbm as lgb
from sklearn import preprocessing, metrics, ensemble, neighbors, linear_model, tree
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn import manifold, decomposition
from sklearn.random_projection import GaussianRandomProjection, SparseRandomProjection

def create_feature_map(features):
	outfile = open('xgb.fmap', 'w')
	for i, feat in enumerate(features):
		outfile.write('{0}\t{1}\tq\n'.format(i,feat))
	outfile.close()

def runXGB(train_X, train_y, test_X, test_y=None, test_X2=None, feature_names=None, seed_val=0, rounds=500, dep=8, eta=0.03):
	params = {}
	params["objective"] = "binary:logistic"
	params['eval_metric'] = 'logloss'
	params["eta"] = eta
	params["subsample"] = 0.7
	params["min_child_weight"] = 1
	params["colsample_bytree"] = 0.7
	params["max_depth"] = dep
	params["silent"] = 1
	params["seed"] = seed_val
	num_rounds = rounds

	plst = list(params.items())
	xgtrain = xgb.DMatrix(train_X, label=train_y)

	if test_y is not None:
		xgtest = xgb.DMatrix(test_X, label=test_y)
		watchlist = [ (xgtrain,'train'), (xgtest, 'test') ]
		model = xgb.train(plst, xgtrain, num_rounds, watchlist, early_stopping_rounds=100, verbose_eval=20)
	else:
		xgtest = xgb.DMatrix(test_X)
		model = xgb.train(plst, xgtrain, num_rounds)

	if feature_names is not None:
			create_feature_map(feature_names)
			model.dump_model('xgbmodel.txt', 'xgb.fmap', with_stats=True)
			importance = model.get_fscore(fmap='xgb.fmap')
			importance = sorted(importance.items(), key=operator.itemgetter(1), reverse=True)
			imp_df = pd.DataFrame(importance, columns=['feature','fscore'])
			imp_df['fscore'] = imp_df['fscore'] / imp_df['fscore'].sum()
			imp_df.to_csv("imp_feat.txt", index=False)

	pred_test_y = model.predict(xgtest, ntree_limit=model.best_ntree_limit)
	pred_test_y2 = model.predict(xgb.DMatrix(test_X2), ntree_limit=model.best_ntree_limit)

	loss = 0
	if test_y is not None:
		loss = metrics.log_loss(test_y, pred_test_y)
		print loss
		return pred_test_y, loss, pred_test_y2
	else:
		return pred_test_y, loss, pred_test_y2


if __name__ == "__main__":
	train_df = pd.read_csv("./train_feat.csv")
	test_df = pd.read_csv("./test_feat.csv")

	train_id = train_df['id'].values
	test_id = test_df['id'].values
	train_match_string = train_df['StringToMatch'].values
	test_match_string = test_df['StringToMatch'].values
	tr_y = train_df['DV'].values

	cols_to_drop = ["id", "StringToExtract", "StringToMatch", "DV"]
	tr_X = train_df.drop(cols_to_drop, axis=1)
	te_X = test_df.drop(cols_to_drop, axis=1)

	kf = KFold(n_splits=5, shuffle=True, random_state=2017)
	cv_scores = []
	pred_test_full = 0
	pred_val_full = np.zeros(tr_X.shape[0])
	for dev_index, val_index in kf.split(tr_X):
		dev_X, val_X = tr_X.ix[dev_index], tr_X.ix[val_index]
		dev_y, val_y = tr_y[dev_index], tr_y[val_index]

		pred_val, loss, pred_test = runXGB(dev_X, dev_y, val_X, val_y, te_X, rounds=8000, dep=6, feature_names=dev_X.columns.tolist())
	
		pred_val_full[val_index] = pred_val
		pred_test_full = pred_test_full + pred_test
		loss = metrics.log_loss(val_y, pred_val)
		cv_scores.append(loss)
		print cv_scores
	pred_test_full /= 5.

	
	out_df = pd.DataFrame({"id":test_id})
	out_df["StringToExtract"] = test_match_string
	out_df["prob"] = pred_test_full
	out_df = out_df.sort_values(by=["id", "prob"])
	out_df = out_df.drop_duplicates(subset=["id"], keep='last')
	out_df[["id", "StringToExtract"]].to_csv("sub4.csv", index=False)
	

	"""
	out_df = pd.DataFrame({"id":train_id})
	out_df["StringToExtract"] = train_match_string
	out_df["prob"] = pred_val_full
	out_df = out_df.sort_values(by=["id", "prob"])
	out_df = out_df.drop_duplicates(subset=["id"], keep='last')
	out_df[["id", "StringToExtract"]].to_csv("sub3_val_preds.csv", index=False)
	"""
