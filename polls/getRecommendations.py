def getRecommendations(current_users_ratings, other_users_and_ratings):
    most_similar_user = getMostSimilarUser(current_users_ratings, other_users_and_ratings)
    return getTopMoviesFrom(most_similar_user, other_users_and_ratings)


def getMostSimilarUser(current_users_ratings, other_users_and_ratings):
    similarity_scores = {}
    movies_in_common = 0
    for username, other_users_ratings in other_users_and_ratings.items():

        similarity_scores[username] = 0

        for current_users_rating in current_users_ratings:
            for other_users_rating in other_users_ratings:
                if other_users_rating.movie == current_users_rating.movie:
                    movies_in_common += 1
                    similarity_scores[username] += abs(current_users_rating.rating - other_users_rating.rating)
            similarity_scores[username] /= (max(1, movies_in_common))

    most_similar_user = min(other_users_and_ratings.keys(), key=similarity_scores.get)
    return most_similar_user

def getTopMoviesFrom(the_one, other_users_and_ratings):
    for username, ratings in other_users_and_ratings.items():
        if the_one == username:
            ratings.sort(key=lambda x: x.rating, reverse=True)
            sorted_movies = [rating.movie for rating in ratings]
            return sorted_movies

    return ["Didn't find the most similar user : /"]
