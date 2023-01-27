*** Settings ***
Library     ListenerCore.py


*** Test Cases ***
Automatic Listener
    Listener Core    This is the first Argument

External Listener
    Second Component    External Listener

No Listener
    First Component    Tests Listener
