def getRecommendations(current_user_name, users_and_ratings):
    most_similar_user = getMostSimilarUser(current_user_name, users_and_ratings)
    return getUnseenTopMoviesFrom(most_similar_user, users_and_ratings, current_user_name)


def getMostSimilarUser(current_user_name, users_and_ratings):
    similarity_scores = {}
    #print(users_and_ratings)
    for other_username in users_and_ratings:
        if other_username == current_user_name:
            continue
        print("\nLooking for commong movies for current user {} and user {}".format(current_user_name, other_username))

        similarity_scores[other_username] = 0
        # Find the movies this user has in common with other users
        for seen_movies in users_and_ratings[current_user_name]:
            if seen_movies in users_and_ratings[other_username]:
                print("bingo for " + str(seen_movies))
                score1 = users_and_ratings[other_username][seen_movies]
            else:
                print("miss for " + str(seen_movies))
                expected_score = 3
                score1 = expected_score

            score2 = users_and_ratings[current_user_name][seen_movies]
            similarity_scores[other_username] += abs(score1 - score2)

            print(similarity_scores)

    most_similar_user = min(similarity_scores, key=similarity_scores.get)
    print("The most similar user is {}".format(most_similar_user))

    return most_similar_user


def getUnseenTopMoviesFrom(most_similar_user, users_and_ratings, current_user_name):
    topMovies = getTopMoviesFrom(most_similar_user, users_and_ratings)
    print("Top movies {}".format(topMovies))

    unseenTopMovies = []
    seen_movies = users_and_ratings[current_user_name]
    print("Seen movies" + str(seen_movies))
    for movie in topMovies:
        if movie not in seen_movies:
            unseenTopMovies.append(movie)

    print(unseenTopMovies)
    return unseenTopMovies


MAX_SCORE = 5
def getTopMoviesFrom(user, users_and_ratings):
    print("looking for getting top movies from {}".format(user))
    for other_username in users_and_ratings:
        if user == other_username:
            print("ratings for user {}".format(user))
            ratings = users_and_ratings[user]
            topMovies = []
            good_score = MAX_SCORE
            while not topMovies and good_score > 2:
                print("good score is {}".format(good_score))
                topMovies = [title for title in ratings if ratings[title] == good_score]
                print("Top movies: {}".format(topMovies))
                good_score = good_score - 1

            if not topMovies:
                return ["{} does not have any movies with rating 3 or higher".format(user)]
            return topMovies


    return ["Didn't find the most similar user : /"]