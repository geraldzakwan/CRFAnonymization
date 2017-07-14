from random import randint

def anonymize_all_org(normalized_tokenized_output, all_idx):
    for idx in all_idx:
        # Kalo bisa dapet location negara
        # Co reference resolution dari project sebelumnya copy
        # Ni harusnya kalo work dibedain mana company mana org, yaudah ntar
        # x = randint(1,2)
        x = 2
        if(x==1):
            normalized_tokenized_output[idx][0] = 'an organization in the country'
        else:
            normalized_tokenized_output[idx][0] = 'a company in the country'

    return normalized_tokenized_output
