def get_scenario_params(round_number):
    print(round_number)
    # Zwraca słownik parametrów do przekazania do funkcji play_video
    if round_number == 1:
        # Scenariusz 1: Wyświetlanie reklamy w całym obszarze gry bez zapowiedzi
        return {
            'time_reset': False,
            'width': 1137,
            'height': 1000,
            'x': 100,
            'y': 20,
            'scenario': "1. Wyświetlanie reklamy w całym obszarze gry bez zapowiedzi"
        }

    elif round_number == 2:
        # Scenariusz 2: Wyświetlanie reklamy w całym obszarze gry z zapowiedzią
        return {
            'time_reset': False,
            'width': 1137,
            'height': 1000,
            'x': 100,
            'y': 20,
            'scenario': "2. Wyświetlanie reklamy w całym obszarze gry z zapowiedzią",
            'prior_notice': True
        }
    elif round_number == 3:
        # Scenariusz 3: Wyświetlanie reklamy w całym obszarze gry z zapowiedzią czasową (np. 5 sekund)
        return {
            'time_reset': False,
            'width': 1137,
            'height': 1000,
            'x': 100,
            'y': 20,
            'scenario': "3. Wyświetlanie reklamy w całym obszarze gry z zapowiedzią czasową (np. 5 sekund)",
            'countdown_before_ad': 5
        }
    elif round_number == 4:
        # Scenariusz 4: Wyświetlanie reklamy w postaci okna pop-up w obszarze gry bez zapowiedzi
        ad_width, ad_height = 600, 400
        ad_x = 100 + (1137 - ad_width) // 2
        ad_y = 20 + (1000 - ad_height) // 2
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "4. Wyświetlanie reklamy w postaci okna pop-up w obszarze gry bez zapowiedzi"
        }
    elif round_number == 5:
        # Scenariusz 5: Wyświetlanie reklamy w postaci okna pop-up w obszarze gry z zapowiedzią
        ad_width, ad_height = 600, 400
        ad_x = 100 + (1137 - ad_width) // 2
        ad_y = 20 + (1000 - ad_height) // 2
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "5. Wyświetlanie reklamy w postaci okna pop-up w obszarze gry z zapowiedzią",
            'prior_notice': True
        }
    elif round_number == 6:
        # Scenariusz 6: Wyświetlanie reklamy w postaci okna pop-up w obszarze gry z zapowiedzią czasową (np. 5 sekund)
        ad_width, ad_height = 600, 400
        ad_x = 100 + (1137 - ad_width) // 2
        ad_y = 20 + (1000 - ad_height) // 2
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "6. Wyświetlanie reklamy w postaci okna pop-up w obszarze gry z zapowiedzią czasową (np. 5 sekund)",
            'countdown_before_ad': 5
        }
    elif round_number == 7:
        # Scenariusz 7: Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry bez zapowiedzi
        ad_width, ad_height = 600, 400
        ad_x = 1240  # Obok obszaru gry
        ad_y = 200
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "7. Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry bez zapowiedzi"
        }
    elif round_number == 8:
        # Scenariusz 8: Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry z zapowiedzią
        ad_width, ad_height = 600, 400
        ad_x = 1240
        ad_y = 200
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "8. Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry z zapowiedzią",
            'prior_notice': True
        }
    elif round_number == 9:
        # Scenariusz 9: Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry z zapowiedzią czasową (np. 5 sekund)
        ad_width, ad_height = 600, 400
        ad_x = 1240
        ad_y = 200
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "9. Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry z zapowiedzią czasową (np. 5 sekund)",
            'countdown_before_ad': 5
        }
    elif round_number == 10:
        # Scenariusz 10: Wyświetlanie reklamy w całym obszarze gry bez zapowiedzi oraz możliwością pominięcia w ciągu 5 sekund
        return {
            'time_reset': False,
            'width': 1137,
            'height': 1000,
            'x': 100,
            'y': 20,
            'scenario': "10. Wyświetlanie reklamy w całym obszarze gry bez zapowiedzi oraz możliwością pominięcia w ciągu 5 sekund",
            'skip_after': 5
        }
    elif round_number == 11:
        # Scenariusz 11: Wyświetlanie reklamy w całym obszarze gry z zapowiedzią oraz możliwością pominięcia w ciągu 5 sekund
        return {
            'time_reset': False,
            'width': 1137,
            'height': 1000,
            'x': 100,
            'y': 20,
            'scenario': "11. Wyświetlanie reklamy w całym obszarze gry z zapowiedzią oraz możliwością pominięcia w ciągu 5 sekund",
            'prior_notice': True,
            'skip_after': 5
        }
    elif round_number == 12:
        # Scenariusz 12: Wyświetlanie reklamy w całym obszarze gry z zapowiedzią czasową (np. 5 sekund) oraz możliwością pominięcia w ciągu 5 sekund
        return {
            'time_reset': False,
            'width': 1137,
            'height': 1000,
            'x': 100,
            'y': 20,
            'scenario': "12. Wyświetlanie reklamy w całym obszarze gry z zapowiedzią czasową (np. 5 sekund) oraz możliwością pominięcia w ciągu 5 sekund",
            'countdown_before_ad': 5,
            'skip_after': 5
        }
    elif round_number == 13:
        # Scenariusz 13: Wyświetlanie reklamy w postaci okna pop-up w obszarze gry bez zapowiedzi oraz możliwością pominięcia w ciągu 5 sekund
        ad_width, ad_height = 600, 400
        ad_x = 100 + (1137 - ad_width) // 2
        ad_y = 20 + (1000 - ad_height) // 2
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "13. Wyświetlanie reklamy w postaci okna pop-up w obszarze gry bez zapowiedzi oraz możliwością pominięcia w ciągu 5 sekund",
            'skip_after': 5
        }
    elif round_number == 14:
        # Scenariusz 14: Wyświetlanie reklamy w postaci okna pop-up w obszarze gry z zapowiedzią oraz możliwością pominięcia w ciągu 5 sekund
        ad_width, ad_height = 600, 400
        ad_x = 100 + (1137 - ad_width) // 2
        ad_y = 20 + (1000 - ad_height) // 2
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "14. Wyświetlanie reklamy w postaci okna pop-up w obszarze gry z zapowiedzią oraz możliwością pominięcia w ciągu 5 sekund",
            'prior_notice': True,
            'skip_after': 5
        }
    elif round_number == 15:
        # Scenariusz 15: Wyświetlanie reklamy w postaci okna pop-up w obszarze gry z zapowiedzią czasową (np. 5 sekund) oraz możliwością pominięcia w ciągu 5 sekund
        ad_width, ad_height = 600, 400
        ad_x = 100 + (1137 - ad_width) // 2
        ad_y = 20 + (1000 - ad_height) // 2
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "15. Wyświetlanie reklamy w postaci okna pop-up w obszarze gry z zapowiedzią czasową (np. 5 sekund) oraz możliwością pominięcia w ciągu 5 sekund",
            'countdown_before_ad': 5,
            'skip_after': 5
        }
    elif round_number == 16:
        # Scenariusz 16: Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry bez zapowiedzi oraz możliwością pominięcia w ciągu 5 sekund
        ad_width, ad_height = 600, 400
        ad_x = 1240  # Obok obszaru gry
        ad_y = 200
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "16. Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry bez zapowiedzi oraz możliwością pominięcia w ciągu 5 sekund",
            'skip_after': 5
        }
    elif round_number == 17:
        # Scenariusz 17: Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry z zapowiedzią oraz możliwością pominięcia w ciągu 5 sekund
        ad_width, ad_height = 600, 400
        ad_x = 1240
        ad_y = 200
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "17. Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry z zapowiedzią oraz możliwością pominięcia w ciągu 5 sekund",
            'prior_notice': True,
            'skip_after': 5
        }
    elif round_number == 18:
        # Scenariusz 18: Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry z zapowiedzią czasową (np. 5 sekund) oraz możliwością pominięcia w ciągu 5 sekund
        ad_width, ad_height = 600, 400
        ad_x = 1240
        ad_y = 200
        return {
            'time_reset': False,
            'width': ad_width,
            'height': ad_height,
            'x': ad_x,
            'y': ad_y,
            'scenario': "18. Wyświetlanie reklamy w postaci okna pop-up obok obszaru gry z zapowiedzią czasową (np. 5 sekund) oraz możliwością pominięcia w ciągu 5 sekund",
            'countdown_before_ad': 5,
            'skip_after': 5
        }
    else:
        # Brak reklamy dla pozostałych rund
        return None
