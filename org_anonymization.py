from random import randint

def anonymize_all_org(normalized_tokenized_output, all_idx):
    # print(all_idx)
    for idx in all_idx:
        # Kalo bisa dapet location negara
        # Co reference resolution dari project sebelumnya copy
        # Ni harusnya kalo work dibedain mana company mana org, yaudah ntar
        # x = randint(1,2)
        # x = 2
        # if(x==1):
        #     normalized_tokenized_output[idx][0] = 'an organization in the country'
        # else:
        #     normalized_tokenized_output[idx][0] = 'college'
        #     normalized_tokenized_output[idx][0] = 'a company in the country'
        phrase = all_idx[idx]
        # print phrase
        # Ini bisa ngambil dari private organizational verbs database
        if("studi" in phrase or "learn" in phrase or "go" in phrase):
            normalized_tokenized_output[idx][0] = 'a university'
        elif("member" in phrase or "belong" in phrase or "volunt" in phrase):
            normalized_tokenized_output[idx][0] = 'an organization'
        elif("work" in phrase or "job" in phrase or "employe" in phrase):
            normalized_tokenized_output[idx][0] = 'a company'
        else:
            org = normalized_tokenized_output[idx][0].lower()
            if ("institution" in org or "institute" in org):
                normalized_tokenized_output[idx][0] = 'an institution'
            elif ("univ" in org or "university" in org):
                normalized_tokenized_output[idx][0] = 'a university'
            elif ("college" in org):
                normalized_tokenized_output[idx][0] = 'a college'
            elif ("organization" in org or "org" in org):
                normalized_tokenized_output[idx][0] = 'an organization'
            elif ("foundation" in org):
                normalized_tokenized_output[idx][0] = 'a foundation'
            else:
                normalized_tokenized_output[idx][0] = 'a company'

    return normalized_tokenized_output

def anonymize_all_event(normalized_tokenized_output, all_idx):
    # print(all_idx)
    for idx in all_idx:
        # Kalo bisa dapet location negara
        # Co reference resolution dari project sebelumnya copy
        # Ni harusnya kalo work dibedain mana company mana org, yaudah ntar
        # x = randint(1,2)
        # x = 2
        # if(x==1):
        #     normalized_tokenized_output[idx][0] = 'an organization in the country'
        # else:
        #     normalized_tokenized_output[idx][0] = 'college'
        #     normalized_tokenized_output[idx][0] = 'a company in the country'
        phrase = all_idx[idx]
        # print phrase
        # Ini bisa ngambil dari private organizational verbs database
        if ("music" in phrase or "musical" in phrase or "concert" in phrase):
            normalized_tokenized_output[idx][0] = 'a music event'
        if ("sport" in phrase or "football" in phrase or "soccer" in phrase or "basketball" in phrase or "match" in phrase):
            normalized_tokenized_output[idx][0] = 'a sport event'
        elif ("charity" in phrase):
            normalized_tokenized_output[idx][0] = 'a charity event'
        else:
            org = normalized_tokenized_output[idx][0].lower()
            if ("music" in org or "musical" in org or "concert" in org):
                normalized_tokenized_output[idx][0] = 'a music event'
            if ("sport" in org or "football" in org or "soccer" in org or "basketball" in org or "match" in org):
                normalized_tokenized_output[idx][0] = 'a sport event'
            elif ("charity" in org):
                normalized_tokenized_output[idx][0] = 'a charity event'
            else:
                normalized_tokenized_output[idx][0] = 'an event'

    return normalized_tokenized_output
