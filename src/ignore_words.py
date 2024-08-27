IGNORE_WORDS = {
    'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit', 'sed', 'do', 'eiusmod', 'tempor',
    'incididunt', 'ut', 'labore', 'et', 'dolore', 'magna', 'aliqua', 'ut', 'enim', 'ad', 'minim', 'veniam', 'quis',
    'nostrud', 'exercitation', 'ullamco', 'laboris', 'nisi', 'ut', 'aliquip', 'ex', 'ea', 'commodo', 'consequat',
    'islorem',

    'duis', 'aute', 'irure', 'dolor', 'in', 'reprehenderit', 'in', 'voluptate', 'velit', 'esse', 'cillum', 'dolore',
    'eu', 'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint', 'occaecat', 'cupidatat', 'non', 'proident', 'sunt', 'in',
    'culpa', 'qui', 'officia', 'deserunt', 'mollit', 'anim', 'id', 'est', 'laborum',

    'gradientbased', 'icmr', 'libro', 'kiano', 'acm', 'hezel', 'gpr1200', 'immersive', 'navigu', '2d', 'vbs24', 'creg',
    'mmm', 'lifelog', 'klaus', 'similaritybased', 'uwe', 'picarrange', 'schall', '30th', 'eisert', 'impressum',
    'datenschutz', 'lsc', 'htw', 'wikimedia', 'nico', 'generalpurpose', 'jung', 'konstantin', 'icmr24', 'datasets',
    '7th', 'florian', 'texttoimage', 'contentbased', 'barthel', 'highdimensional', 'vbs', 'runnerup', 'vibro', 'bruno',
    'tim', 'kai',

    'similars', 'akiwi', 'picsbuffet', 'imagex', 'imagesorter', 'wikiviewnet', 'apetopia',

    'pretraining', 'navigunet', 'visapp', 'dataset', 'lindemann', 'andreas', '27th', 'neumann', 'christopher', 'möller',
    'lowlevel', 'farbunterschiede', 'selfsorting', '28th', 'andy', 'ssm', 'dpq', 'richter', 'searchbyexample',
    'convolutional', '12th', 'moritz', 'flas', 'unindexed', 'radek', 'anuj', '2nd', 'arxiv', 'ieee', 'analytics',
    '22nd', 'imagemap', '64byte', 'metadata', '29th', 'dont', 'wiley', 'nra', 'follmann', 'subimage', 'adhoc',
    'largescale', 'subgraphs', 'finetuned', 'angewandter', 'christine', 'shotdetection', '21st', 'imagetoimage',
    'mackowiak', 'zeroshot', 'zur', 'zoomable', 'maplike', 'deg', 'localprivate', 'draggable', 'klack', 'goyal',
    'userfriendly', 'mm', 'highquality', 'imur', 'wiederer', 'vbs2021', 'paris', 'inria', 'realtime', 'ein', 'mmsp',
    'highlevel', '24th', 'ltd', 'interimage', 'keywording', 'knn', 'erfassung', 'userperceived', 'empfundener',
    'müller', 'farbbildverarbeitung', 'informatik', 'visigrapp', 'förderung', 'spielerisches', 'imagex', 'backstein',
    'fws', 'siggraph', 'david', 'stateoftheart', 'runtime', 'sebastian', 'finetuning',

    'kaiuwe', 'wikiview', 'dring',

    'knorr', 'pixolution', 'eah', 'msc', 'co', 'tu', 'phd', 'trans', 'sc', 'pixolutions', 'jpeg', '2dto3d', 'ui',
    'imcube', 'rd', 'jena', 'gmbh', 'visionvisual', 'luratech', 'fktg', '3d', 'stereographer', 'tokyo', 'livestream',
    'bsc', 'visualcomputing', 'jpeg2000', 'kk', 'cbmi', 'ceo', 'postconversion', 'dublin', 'tv', 'beijing', 'kais',
    'ee', 'ag', 'dr', 'inc',

    'ikea', 'january', 'ecommerce',

    'zürich', 'islorem', 'doubleclick', 'imagenet', 'eth', 'antworten', 'und', 'fragen', 'app', 'pixabay',
    'httpsnavigunet', 'sourcespixabay',

    'pdf', 'slideshow', 'deutsch', 'usb', 'app', 'multicolumn', 'macos', 'subfolders', 'youre', 'youtube', 'iosmacos',
    'macossupported', 'videotag', 'hd', 'doesnt', 'github', 'domainrich', 'instre', 'icloud', 'youve', 'youve',
    'ipados', 'slideshows', 'wwwdatascienceblogcom', 'iosipados', 'ios', 'tldr', 'bruteforce', 'phuket', 'fraunhofer',
    'twodimensional', 'google', 'bibtex', 'workflow', 'pretrained', 'anns'
}


def ignore_word(word) -> bool:
    if not word:
        return True
    if word.endswith('based'):
        return True
    if word in IGNORE_WORDS:
        return True
    return False
