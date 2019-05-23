NO_MATCH_PUNISH = 0.1
UNSEEN_MOVIE_SCORE = 3
MAX_SCORE = 5


def getRecommendations(current_user_name, users_and_ratings):
    most_similar_users = getMostSimilarUsers(current_user_name, users_and_ratings)
    return getUnseenTopMoviesFrom(most_similar_users, users_and_ratings, current_user_name)


def getMostSimilarUsers(current_user_name, users_and_ratings):
    similarity_scores = {}
    for other_username in users_and_ratings:
        if other_username == current_user_name:
            continue
        debugPrint("\nLooking for common movies for current user {} and user {}".format(current_user_name, other_username))

        similarity_scores[other_username] = 0
        # Find the movies this user has in common with other users
        seen_movies = users_and_ratings[current_user_name]
        for seen_movie in seen_movies:
            debugPrint("searching for {}".format(str(seen_movie)))
            score1 = users_and_ratings[current_user_name][seen_movie]
            if seen_movie in users_and_ratings[other_username]:
                debugPrint("bingo for " + str(seen_movie))
                score2 = users_and_ratings[other_username][seen_movie]
                similarity_scores[other_username] += abs(score1 - score2)
            else:
                debugPrint("miss for " + str(seen_movie))
                similarity_scores[other_username] += abs(score1 - UNSEEN_MOVIE_SCORE) + NO_MATCH_PUNISH

            debugPrint("similarity_scores: {}".format(similarity_scores))

    most_similar_users = []
    while similarity_scores:
        most_similar_user = min(similarity_scores, key=similarity_scores.get)
        most_similar_users.append(most_similar_user)
        debugPrint("The most similar users are {}".format(most_similar_users))
        similarity_scores.pop(most_similar_user)

    return most_similar_users


def getUnseenTopMoviesFrom(most_similar_users, users_and_ratings, current_user_name):
    for user in most_similar_users:
        topMovies = getTopMoviesFrom(user, users_and_ratings)
        if topMovies:
            debugPrint("Top movies from {}: {}".format(user, topMovies))
            unseenTopMovies = []
            seen_movies = users_and_ratings[current_user_name]
            debugPrint("Seen movies" + str(seen_movies))
            for movie in topMovies:
                if movie not in seen_movies:
                    unseenTopMovies.append(movie)

            debugPrint("Unseen top movies: {}".format(unseenTopMovies))
            if unseenTopMovies:
                return unseenTopMovies

        else:
            debugPrint("{} didn't have any movies with high enough rating".format(user))

    return ["Rate more movies and ask your friends to do the same to get recommendations :)"]


def getTopMoviesFrom(user, users_and_ratings):
    if not user in users_and_ratings:
        return ["{} does not exist".format(user)]

    debugPrint("looking for top movies from {}".format(user))
    ratings = users_and_ratings[user]
    topMovies = []
    good_score = MAX_SCORE
    while not topMovies and good_score > 2:
        debugPrint("good score is {}".format(good_score))
        topMovies = [title for title in ratings if ratings[title] == good_score]
        debugPrint("Top movies: {}".format(topMovies))
        good_score = good_score - 1

    return topMovies


def debugPrint(mystr):
    DEBUG = True
    if DEBUG:
        print(mystr)