def getRecommendations(current_user, all_users):
    current_user_name = current_user.get_username()

    other_users = [user for user in all_users if user.get_username() != current_user_name]

    most_similar_user = getMostSimilarUser(current_user, other_users)

    return getTopMoviesFrom(most_similar_user)


def getMostSimilarUser(current_user, other_users):
    return other_users[0]  # Don't do anything right now


def getTopMoviesFrom(user):
    return ["lorem", "ipsum",]
