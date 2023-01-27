grammar funx;

root : code EOF ;

code:   createProcedure* (instruction)?;
        
instruction:
        assignation  
        | conditional
        | comparison
        | loops
        | expr
        ;

createProcedure: 
        NAMEPROCEDURE  VAR* '{' instruction* '}'                        # Function
        ;

assignation : 
        VAR ASSIGNMENT (expr|comparison)                                # Declaration
        ;

conditional:
        IF comparison '{' instruction* '}'                              #IfThen
        | IF comparison '{' instruction* '}' ELSE  '{' instruction* '}' #IfThenElse  
        ;

loops:   
        WHILE comparison '{' instruction* '}'                           # while
        | FOR assignation';'comparison';'assignation'{'instruction*'}'  # for
        ;

comparison:
        '(' comparison ')'                                              # BracketsComparison
        | comparison '&' comparison                                     # logicAnd
        | comparison '|' comparison                                     # logicOr  
        | '!' comparison                                                # Not    
        | expr EQ expr                                                  # EqualComparison
        | expr NE expr                                                  # NotEqualComparison
        | expr LET expr                                                 # LessOrEqualThanComparison
        | expr GET expr                                                 # GreaterOrEqualThanComparison
        | expr LT expr                                                  # LessThanComparison
        | expr GT expr                                                  # GreaterThanComparison
        | TRUE                                                          # True
        | FALSE                                                         # False
        ;
expr :  
        '(' expr ')'                                                    # BracketsExpression
        | NAMEPROCEDURE expr*                                           # FunctionCall
        | <assoc=right> expr POWER expr                                 # Power     
        | expr PROD expr                                                # Product     
        | expr DIV expr                                                 # Division 
        | expr MOD expr                                                 # Modul   
        | expr MENYS expr                                               # Substraction
        | expr MES expr                                                 # Addition
        | MENYS expr                                                    # Minus   
        | FLOAT                                                         # LiteralFloat
        | NUM                                                           # Literal
        | VAR                                                           # Variable
        ;

// funcions
NAMEPROCEDURE: [A-Z]([a-zA-Z0-9\u0080-\u00FF] |'_')*;
RETURN: 'return';

ASSIGNMENT: '<-';

// operadors booleans
NE : '!=';
EQ : '=';
LT : '<';
GT: '>';
LET : '<=';
GET: '>=';
TRUE: 'true';
FALSE: 'false';


// condicionals
IF : 'if';
THEN: 'then';
ELSE: 'else';

// bucles
WHILE: 'while';
FOR: 'for';

// aritmetica
FLOAT: NUM + '.' NUM*;
NUM : [0-9]+ ;
MES : '+' ;
MENYS : '-';
PROD: '*';
DIV: '/';
POWER: '^';
MOD: '%';

// variables i assignacio
VAR:  [a-z]+;

COMMENT: '#' ~[\r\n]* -> skip ;
WS : [ \r\n]+ -> skip;