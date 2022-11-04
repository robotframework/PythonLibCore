*** Settings ***
Library     DynamicTypesLibrary.py
Library     DynamicTypesAnnotationsLibrary.py    xxx


*** Variables ***
${CUSTOM NONE} =    ${None}


*** Test Cases ***
Keyword Default Argument As Abject None
    ${return} =    DynamicTypesLibrary.Keyword None    ${None}
    Should Match Regexp    ${return}    None: <(class|type) 'NoneType'>

Keyword Default Argument As Abject None Default Value
    ${return} =    DynamicTypesLibrary.Keyword None
    Should Match Regexp    ${return}    None: <(class|type) 'NoneType'>

Keyword Default Argument As String None
    ${return} =    DynamicTypesLibrary.Keyword None    None
    Should Match Regexp    ${return}    None: <(class|type) '(unicode|str|NoneType)'>

Keyword Default As Booleans With Defaults
    ${return} =    DynamicTypesLibrary.Keyword Booleans
    Should Match Regexp    ${return}    True: <(class|type) 'bool'>, False: <(class|type) 'bool'>

Keyword Default As Booleans With Objects
    ${return} =    DynamicTypesLibrary.Keyword Booleans    ${False}    ${True}
    Should Match Regexp    ${return}    False: <(class|type) 'bool'>, True: <(class|type) 'bool'>

Keyword Annonations And Bool Defaults Using Default
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Default And Annotation    42
    Should Match Regexp    ${return}    42: <(class|type) 'int'>, False: <(class|type) 'bool'>

Keyword Annonations And Bool Defaults Defining All Arguments
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Default And Annotation    1    true
    Should Match Regexp    ${return}    1: <(class|type) 'int'>, true: <(class|type) 'str'>

Keyword Annonations And Bool Defaults Defining All Arguments And With Number
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Default And Annotation    ${1}    true
    Should Match Regexp    ${return}    1: <(class|type) 'int'>, true: <(class|type) 'str'>

Keyword Annonations And Robot Types Disbales Argument Conversion
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Robot Types Disabled And Annotations    111
    Should Match Regexp    ${return}    111: <(class|type) 'str'>

Keyword Annonations And Keyword Only Arguments
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Only Arguments    1    ${1}    some=222
    Should Match Regexp    ${return}    \\('1', 1\\): <class 'tuple'>, 222: <class '(int|str)'>

Keyword Only Arguments Without VarArg
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Only Arguments No Vararg    other=tidii
    Should Match    ${return}    tidii: <class 'str'>

Varargs and KeywordArgs With Typing Hints
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Self And Keyword Only Types
    ...    this_is_mandatory    # mandatory argument
    ...    1    2    3    4    # varargs
    ...    other=True    # other argument
    ...    key1=1    key2=2    # kwargs
    Should Match
    ...    ${return}
    ...    this_is_mandatory: <class 'str'>, (1, 2, 3, 4): <class 'tuple'>, True: <class 'bool'>, {'key1': 1, 'key2': 2}: <class 'dict'>

Enum Conversion Should Work
    ${value} =    Enum Conversion    ok
    Should Match    OK penum.ok    ${value}

Enum Conversion To Invalid Value Should Fail
    Run Keyword And Expect Error    ValueError: Argument 'param' got value 'not ok' that*
    ...    Enum Conversion    not ok

Type Conversion With Optional And None
    ${types} =    Keyword Optional With None
    Should Contain    ${types}    arg: None,
    Should Contain    ${types}    <class 'NoneType'>
    ${types} =    Keyword Optional With None    None
    Should Contain    ${types}    arg: None,
    Should Contain    ${types}    <class 'str'>
    ${types} =    Keyword Optional With None    ${None}
    Should Contain    ${types}    arg: None,
    Should Contain    ${types}    <class 'NoneType'>
    ${types} =    Keyword Optional With None    arg=${CUSTOM NONE}
    Should Contain    ${types}    arg: None,
    Should Contain    ${types}    <class 'NoneType'>

Type Conversion With Union And Multiple Types
    ${types} =    Keyword Union With None
    Should Contain    ${types}    arg: None,
    Should Contain    ${types}    <class 'NoneType'>
    ${types} =    Keyword Union With None    None
    Should Contain    ${types}    arg: None,
    Should Contain    ${types}    <class 'str'>
    ${types} =    Keyword Union With None    {"key": 1}
    Should Contain    ${types}    arg: {"key": 1},
    Should Contain    ${types}    <class 'str'>

Python 3.10 New Type Hints
    [Tags]    py310
    [Setup]    Import DynamicTypesAnnotationsLibrary In Python 3.10 Only
    ${types} =    Python310 Style    111
    ${rf401} =    DynamicTypesLibrary.Is Rf 401
    IF    ${rf401} != ${True}
        Should Be Equal    ${types}    arg: 111, type: <class 'int'>
    ELSE
        Should Be Equal    ${types}    arg: 111, type: <class 'str'>
    END
    ${types} =    Python310 Style    {"key": 1}
    IF    ${rf401} != ${True}
        Should Be Equal    ${types}    arg: {'key': 1}, type: <class 'dict'>
    ELSE
        Should Be Equal    ${types}    arg: {"key": 1}, type: <class 'str'>
    END


*** Keywords ***
Import DynamicTypesAnnotationsLibrary In Python 3.10 Only
    ${py3} =    DynamicTypesLibrary.Is Python 3 10
    IF    ${py3}    Import Library    Python310Library.py
