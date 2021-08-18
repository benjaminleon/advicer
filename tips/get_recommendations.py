NO_MATCH_PUNISH = 0.1
UNSEEN_MOVIE_SCORE = 3
MAX_SCORE = 5


def get_recommendations(current_user_name, users_and_ratings):
    if current_user_has_no_ratings(current_user_name, users_and_ratings):
        return []
    most_similar_users = get_most_similar_users(current_user_name, users_and_ratings)
    return get_unseen_top_movies_from(
        most_similar_users, users_and_ratings, current_user_name
    )


def current_user_has_no_ratings(current_user_name, users_and_ratings):
    return not users_and_ratings[current_user_name]


def get_most_similar_users(current_user_name, users_and_ratings):
    similarity_scores = {}
    for other_username in users_and_ratings:
        if other_username == current_user_name:
            continue
        debug_print(f"\nLooking for common movies for current user {current_user_name} and user {other_username}")

        similarity_scores[other_username] = 0
        # Find the movies this user has in common with other users
        seen_movies = users_and_ratings[current_user_name]
        for seen_movie in seen_movies:
            debug_print(f"searching for {seen_movie}")
            score1 = users_and_ratings[current_user_name][seen_movie]
            if seen_movie in users_and_ratings[other_username]:
                debug_print(f"bingo for {seen_movie}")
                score2 = users_and_ratings[other_username][seen_movie]
                similarity_scores[other_username] += abs(score1 - score2)
            else:
                debug_print(f"miss for {seen_movie}")
                similarity_scores[other_username] += (
                    abs(score1 - UNSEEN_MOVIE_SCORE) + NO_MATCH_PUNISH
                )

            debug_print(f"similarity scores: {similarity_scores}")

    most_similar_users = []
    while similarity_scores:
        most_similar_user = min(similarity_scores, key=similarity_scores.get)
        most_similar_users.append(most_similar_user)
        debug_print(f"The most similar users are {most_similar_users}")
        similarity_scores.pop(most_similar_user)

    return most_similar_users


def get_unseen_top_movies_from(
    most_similar_users, users_and_ratings, current_user_name
):
    unseen_top_movies = []
    seen_movies = users_and_ratings[current_user_name]
    for user in most_similar_users:
        top_movies = get_top_movies_from(user, users_and_ratings)
        if top_movies:
            debug_print(f"Top movies from {user}: {top_movies}")
            debug_print(f"Seen movies {seen_movies}")
            for movie in top_movies:
                if movie not in seen_movies:
                    unseen_top_movies.append(movie)

            debug_print(f"Unseen top movies: {unseen_top_movies}")
            if len(unseen_top_movies) >= 10:
                return unseen_top_movies

        else:
            debug_print(f"{user} didn't have any movies with {MAX_SCORE} in rating")

    return unseen_top_movies


def get_top_movies_from(user, users_and_ratings):
    if user not in users_and_ratings:
        return [f"{user} does not exist"]

    debug_print(f"looking for top movies from {user}")
    ratings = users_and_ratings[user]
    top_movies = []
    good_score = MAX_SCORE
    while not top_movies and good_score > 2:
        debug_print(f"good score is {good_score}")
        top_movies = [title for title in ratings if ratings[title] == good_score]
        debug_print(f"Top movies: {top_movies}")
        good_score = good_score - 1

    return top_movies


def debug_print(mystr):
    debug = True
    if debug:
        print(mystr)
