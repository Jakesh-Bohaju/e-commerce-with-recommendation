from django.http import request
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import numpy as np
from recommendation.data_collection import read_dataset, hybrid_recommendation, content_based_filtering, \
    collaborative_based_filtering
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
from store.models import Product
from vendor.models import EcommerceUser


#
# def recomevaltry():
#     df_product, df_vendor, df_category, df_user, df_review = read_dataset(request)
#     df_product = df_product.drop(
#         columns=['user_id', 'thumbnail', 'image', 'slug', 'price', 'description', 'status', 'category_id', ])
#     df_review = df_review.drop(columns=['id', 'created_at']).rename(
#         columns={'product_id': 'id', 'created_by_id': 'user_id'})
#     df = pd.merge(df_product, df_review, on="id", how="left").dropna()
#     df['reviews'] = df['content']
#     df = df.drop(['content'], axis=1)
#     relevant_columns = ['user_id', 'id', 'rating']
#     df = df[relevant_columns]
#     count_rating = (
#         df.groupby(by=['id'])['rating'].count().reset_index().rename(columns={'rating': 'rating_count'})[
#             ['id', 'rating_count']]
#     )
#     df_new = pd.merge(df, count_rating, on="id", how="left").dropna()
#     df_new = df_new.drop_duplicates(['user_id', 'id'])
#     df_new_pvt = df_new.pivot(index='id', columns='user_id', values='rating').fillna(0)
#     df_new_pvt_matrix = csr_matrix(df_new_pvt.values)
#     df = df_new_pvt_matrix
#     print(df)
#     # df = df.T.to_dict().values()
#     train_df, test_df = train_test_split(df, test_size=0.2)
#     # train = train_df.T.to_dict().values()
#     # test = test_df.T.to_dict().values()
#
#     # actual_items = {}
#     # for entry in test_df:
#     #     user = entry['user_id']
#     #     item = entry['id']
#     #     if user not in actual_items:
#     #         actual_items[user] = []
#     #     actual_items[user].append(item)
#     # k = 3
#     # model_knn = NearestNeighbors(n_neighbors=k, metric='cosine', algorithm='brute')
#     # model_knn.fit(train_df)
#     model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
#     model_knn.fit(train_df)
#
#     precision_scores = []
#     recall_scores = []
#     f1_scores = []
#
#     for test_user_items in test_df:
#         distance, indices = distances, indices = model_knn.kneighbors(
#             test_user_items.reshape(1, -1), n_neighbors=2)
#         recommended_items = train_df[indices[0]]
#
#         # Convert the recommended items to binary (0 or 1)
#         binary_recommended_items = [1 if item >= 0.5 else 0 for item in recommended_items[0]]
#
#         precision_scores.append(precision_score(test_user_items, binary_recommended_items))
#         recall_scores.append(recall_score(test_user_items, binary_recommended_items))
#         f1_scores.append(f1_score(test_user_items, binary_recommended_items))
#
#     average_precision = sum(precision_scores) / len(precision_scores)
#     average_recall = sum(recall_scores) / len(recall_scores)
#     average_f1 = sum(f1_scores) / len(f1_scores)
#
#     print("Precision:", average_precision)
#     print("Recall:", average_recall)
#     print("F1-score:", average_f1)
#
#     # import random
#     # predicted_items = {}
#     # for entry in test:
#     #     user = entry['user_id']
#     #     if user not in predicted_items:
#     #         predicted_items[user] = []
#     #     recommended_item = random.choice(['user_id', 'id', 'rating'])
#     #     predicted_items[user].append(recommended_item)
#     #
#     # print("actual", actual_items)
#     # print("predict", predicted_items)
#     #
#     # def evaluate_recommendation_system(actual_items, predicted_items):
#     #     # Flatten the actual and predicted items
#     #     actual_labels = [item for items in actual_items.values() for item in items]
#     #     predicted_labels = [item for items in predicted_items.values() for item in items]
#     #
#     #     # Calculate precision
#     #     precision = precision_score(actual_labels, predicted_labels, average='micro')
#     #
#     #     # Calculate recall
#     #     recall = recall_score(actual_labels, predicted_labels, average='micro')
#     #
#     #     # Calculate F1-score
#     #     f1 = f1_score(actual_labels, predicted_labels, average='micro')
#     #
#     #     # Calculate accuracy
#     #     accuracy = accuracy_score(actual_labels, predicted_labels)
#     #
#     #     return precision, recall, f1, accuracy
#     #
#     # # # Example actual items
#     # # actual_items = {
#     # #     'user1': ['item1', 'item3', 'item4'],
#     # #     'user2': ['item2', 'item5'],
#     # #     'user3': ['item1', 'item4']
#     # # }
#     # #
#     # # # Example predicted items by the recommendation system
#     # # predicted_items = {
#     # #     'user1': ['item1', 'item2', 'item3'],
#     # #     'user2': ['item2', 'item4', 'item5'],
#     # #     'user3': ['item1', 'item3', 'item5']
#     # # }
#     #
#     # precision, recall, f1, accuracy = evaluate_recommendation_system(actual_items, predicted_items)
#     # print("Precision:", precision)
#     # print("Recall:", recall)
#     # print("F1-score:", f1)
#     # print("Accuracy:", accuracy)
def kkk():
    recomm_prod = []
    # users = EcommerceUser.objects.filter(is_superuser=False, is_vendor=False)
    con_score = []
    col_distance = []
    products = Product.objects.all()
    for i in products:
        n_pid, con_pid_df = content_based_filtering(request, i.id)
        coll_pid, coll_pid_df = collaborative_based_filtering(request, i.id)
        con_pid, coll_pid, hyb_pid = hybrid_recommendation(request, i.id)
        if con_pid_df is not None:
            con_score.append(con_pid_df['score'])
        else:
            continue

        if not hyb_pid == None:
            recommended_products = Product.objects.filter(id__in=hyb_pid[1:6], status='Active')
            recomm_prod.append([pid.id for pid in recommended_products])
        elif not coll_pid == None:
            recommended_products = Product.objects.filter(id__in=coll_pid[1:6], status='Active')
            recomm_prod.append([pid.id for pid in recommended_products])
        elif not con_pid == None:
            recommended_products = Product.objects.filter(id__in=con_pid[1:6], status='Active')
            recomm_prod.append([pid.id for pid in recommended_products])

        else:
            pass
    con_score = np.mean(con_score)
    print(con_score)
    coverage_score = coverage(recomm_prod)
    print("sc ", coverage_score*100)
    print("score", coverage_score / con_score * 100)
    coverage_score = coverage_score / con_score * 100
    return coverage_score


def coverage(recommended_items):
    all_recommended_items = [item for sublist in recommended_items for item in sublist]
    unique_items = set(all_recommended_items)
    coverage_score = len(unique_items) / len(all_recommended_items)
    return coverage_score


def simprod():
    df_product, df_vendor, df_category, df_user, df_review = read_dataset(request)
    df_product = df_product.drop(
        columns=['user_id', 'thumbnail', 'image', 'slug', 'price', 'description', 'status', 'category_id', ])
    df_review = df_review.drop(columns=['id', 'created_at']).rename(
        columns={'product_id': 'id', 'created_by_id': 'user_id'})
    df = pd.merge(df_product, df_review, on="id", how="left").dropna()
    df['reviews'] = df['content']
    df = df.drop(['content'], axis=1)
    relevant_columns = ['user_id', 'id', 'rating']
    df = df[relevant_columns]
    # count_rating = (
    #     df.groupby(by=['id'])['rating'].count().reset_index().rename(columns={'rating': 'rating_count'})[
    #         ['id', 'rating_count']]
    # )
    # df_new = pd.merge(df, count_rating, on="id", how="left").dropna()
    # df_new = df_new.drop_duplicates(['user_id', 'id'])
    # df_new_pvt = df_new.pivot(index='id', columns='user_id', values='rating').fillna(0)
    # df_new_pvt_matrix = csr_matrix(df_new_pvt.values)
    # df = df_new_pvt_matrix
    # print(df)
    pvt = df.pivot_table(index='user_id', columns='id', values='rating').fillna(0)
    print(pvt)

    # Example user-clicked product
    clicked_product_index = 0

    # Calculate pairwise cosine similarity between products
    product_similarity = cosine_similarity(df.T)

    # Retrieve similar products based on the clicked product
    similar_products_indices = product_similarity[clicked_product_index].argsort()[::-1]

    # Exclude the clicked product itself
    similar_products_indices = similar_products_indices[similar_products_indices != clicked_product_index]

    # Get similar product IDs
    similar_products = similar_products_indices.tolist()

    print("Similar Products:", similar_products)

#
# def f1_score_at_k(actual_items, recommended_items, k):
#     # Convert the recommended items list up to position K
#     recommended_at_k = recommended_items[:k]
#
#     # Calculate precision at K
#     precision = len(set(actual_items) & set(recommended_at_k)) / float(len(recommended_at_k))
#
#     # Calculate recall at K
#     recall = len(set(actual_items) & set(recommended_at_k)) / float(len(actual_items))
#
#     # Calculate F1 score at K
#     if precision + recall != 0:
#         f1_score = 2 * (precision * recall) / (precision + recall)
#     else:
#         f1_score = 0.0
#
#     return f1_score
