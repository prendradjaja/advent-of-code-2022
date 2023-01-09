import re


def sscanf(s, fmt):
    '''
    Parses the string against the given template, returning the values of the
    slots. If no match, return None.

    The string must be a full match (like re.fullmatch()).

    Each slot is parsed non-greedily. (Is this a good approach?)

    Supported placeholders:
    %s: Scan a string. Unlike C sscanf(), the scan is not terminated at
        whitespace.
    %u: Scan for a positive ("unsigned") decimal integer.

    TODO Add support for %d

    >>> sscanf(
    ...     'The quick brown fox jumped over 2 lazy dogs',
    ...     'The %s brown fox jumped over %u lazy dogs',
    ... )
    ('quick', 2)

    >>> sscanf(
    ...     'quick fox, 2 dogs, 31 cats, wow!',
    ...     '%s fox, %u dogs, %u cats, %s',
    ... )
    ('quick', 2, 31, 'wow!')

    >>> sscanf(
    ...     'quick fox, 2 dogs, 31 cats',
    ...     '%s fox, %u dogs, %u cats, %s',
    ... ) == None
    True
    '''
    # Parse `fmt` into `pattern`
    slot_pattern = r'(%s|%u)'
    pattern = ''
    slot_types = []
    for part in re.split(slot_pattern, fmt):
        is_slot = bool(re.fullmatch(slot_pattern, part))
        if is_slot:
            slot_types.append(part)
            if part == '%s':
                pattern += r'(.+?)'
            elif part == '%u':
                pattern += r'(\d+?)'
            else:
                1/0  # Invalid placeholder
        else:
            pattern += re.escape(part)

    # Try to match
    match = re.fullmatch(pattern, s)
    if not match:
        return None

    # If match, parse values and return
    result = ()
    for raw_value, slot_type in zip(match.groups(), slot_types):
        if slot_type == '%s':
            value = raw_value
        elif slot_type == '%u':
            value = int(raw_value)
        result += (value,)
    return result
