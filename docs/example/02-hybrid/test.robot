*** Settings ***
Library    HybridLibrary

*** Test Cases ***
Join Stings
    ${data} =    Join Strings    kala    is     big
    Should Be Equal    ${data}    kala is big

Sum Values
    ${data} =    Sum    1    2
    Should Be Equal As Numbers    ${data}    3

Wait Something To Happen
    ${data} =    Wait Something To Happen    tidii    3
    Should Be Equal    ${data}    tidii tidii and 6

Join Strings With Separator
    ${data} =    Join String With Separator    Foo    Bar   Tidii   separator=|-|
    Should Be Equal    ${data}    Foo|-|Bar|-|Tidii
    ${data} =    Join String With Separator    Foo    Bar   Tidii
    Should Be Equal    ${data}    Foo;Bar;Tidii

Waiter Is Not Keyword
    Run Keyword And Expect Error
    ...    No keyword with name 'Waiter' found.
    ...    Waiter    1.0