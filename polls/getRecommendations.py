def getRecommendations(current_users_ratings, other_users_and_ratings):
    most_similar_user = getMostSimilarUser(current_users_ratings, other_users_and_ratings)
    return getTopMoviesFrom(most_similar_user)


def getMostSimilarUser(current_users_ratings, other_users_and_ratings):
    print("looking for most similar user among {}".format(list(other_users_and_ratings.keys())))

    for username, rating in other_users_and_ratings.items():
        print(username)
        print(rating)

        # Implement algorithm here

    return list(other_users_and_ratings.keys())[0]  # Don't do anything right now


def getTopMoviesFrom(user):
    return ["lorem", "ipsum",]
