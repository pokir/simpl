%require "3.8"
%language "c++"
%token END 0
%token RETURN "->"
%token IDENTIFIER NUMERIC_LITERAL STRING_LITERAL BOOLEAN_LITERAL
%token DUPLICATE ".."
%token OR "||" AND "&&"
%token LESS_EQUAL "<=" GREATER_EQUAL ">=" EQUAL "==" NOT_EQUAL "!="
%right '@'
%right '?' ':'
%right '&'
%left '!'
%%

statement:
         block '}'
|        expression '.'
|        '@' IDENTIFIER
|        '@'
|        DUPLICATE
|        '&' block
|        '?' statement
|        '?' statement ':' statement
|        IDENTIFIER '!'
|        RETURN
|        '^'
|        '+'
|        '-'
|        '*'
|        '/'
|        '%'
|        '<'
|        '>'
|        LESS_EQUAL
|        GREATER_EQUAL
|        EQUAL
|        NOT_EQUAL
|        OR
|        AND
;

block:
     '{'
|    block statement

expression:
          IDENTIFIER
|         NUMERIC_LITERAL
|         STRING_LITERAL
|         BOOLEAN_LITERAL
;
