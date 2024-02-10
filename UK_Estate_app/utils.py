def range_price_buckets(filtered_price):
    first_category = 0
    second_category = 0
    third_category = 0
    fourth_category = 0
    fifth_category = 0
    sixth_category = 0

    price_ranger_dict = {

    }

    for price in filtered_price:
        price = price.replace(",", "")
        if 100 < float(price) < 1000:
            first_category += 1
            price_ranger_dict['100 - 1000'] = first_category
        elif 1000 < float(price) < 10000:
            second_category += 1
            price_ranger_dict['1000 - 10 000'] = second_category
        elif 10000 < float(price) < 100000:
            third_category += 1
            price_ranger_dict['10 000 - 100 000'] = third_category
        elif 100000 < float(price) < 1000000:
            fourth_category += 1
            price_ranger_dict['100 000 - 1 000 000'] = fourth_category
        elif 1000000 < float(price) < 10000000:
            fifth_category += 1
            price_ranger_dict['1 000 000 - 10 000 000'] = fifth_category
        elif 10000000 < float(price) < 100000000:
            sixth_category += 1
            price_ranger_dict['10 000 000 - 100 000 000'] = sixth_category

    final_res_dict = {k: v for k, v in price_ranger_dict.items() if v != 0}

    return sorted(final_res_dict.keys())
