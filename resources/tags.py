valid_tags = {
    'dev': 'dev',
    'test': 'test',
    'prod': 'prod'
}


def get_next_tag(incoming_tag: str) -> str:
    """
    Return the next tag in a sequence. For instance, dev -> test -> prod

    :param incoming_tag: The tag to get the next tag for
    :return: The next tag in the sequence
    """
    if incoming_tag not in valid_tags:
        return None

    if incoming_tag == valid_tags['dev']:
        return valid_tags['test']
    elif incoming_tag == valid_tags['test']:
        return valid_tags['prod']
    else:
        return valid_tags['prod']
