if __name__ is not None and "." in __name__:
    from .funxParser import funxParser
    from .funxVisitor import funxVisitor
else:
    from funxParser import funxParser
    from funxVisitor import funxVisitor

from flask import Flask, render_template, request
from antlr4 import *
from funxLexer import funxLexer
from funxParser import funxParser


"""
PART DEL INTERPRET -------------------------------------------------------------------
"""

# classe que guarda el nom, els parametres i el context d'una funcio


class Procedure():
    def __init__(self, name, params, context):
        self.name = name
        self.params = params
        self.context = context


class funx(funxVisitor):

    def __init__(self):
        self.vars_dictionary = {}
        self.procedures = {}
        self.stack = []
        empty_dict = {}
        self.stack.append(empty_dict)
        # procediments i els seus respectius parametres, per l'aplicacio web
        self.procedures_params = []

    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        return str(self.visit(l[0]))

    """
        ------------------------------------------------------------
        OPERACIONS ARITMETIQUES ------------------------------------
        ------------------------------------------------------------
        """

    # Visit a parse tree produced by funxParser#BracketsExpression.
    def visitBracketsExpression(
            self, ctx: funxParser.BracketsExpressionContext):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    # Visit a parse tree produced by funxParser#Substraction.
    def visitSubstraction(self, ctx: funxParser.SubstractionContext):
        l = list(ctx.getChildren())
        return self.visit(l[0]) - self.visit(l[2])

    # Visit a parse tree produced by funxParser#Addition.
    def visitAddition(self, ctx: funxParser.AdditionContext):
        l = list(ctx.getChildren())
        return self.visit(l[0]) + self.visit(l[2])

    # Visit a parse tree produced by funxParser#Literal.
    def visitLiteral(self, ctx: funxParser.LiteralContext):
        l = list(ctx.getChildren())
        return int(l[0].getText())

    # Visit a parse tree produced by funxParser#LiteralFloat.
    def visitLiteralFloat(self, ctx: funxParser.LiteralFloatContext):
        l = list(ctx.getChildren())
        return float(l[0].getText())

    # Visit a parse tree produced by funxParser#Product.
    def visitProduct(self, ctx: funxParser.ProductContext):
        l = list(ctx.getChildren())
        return self.visit(l[0]) * self.visit(l[2])

    # Visit a parse tree produced by funxParser#Division.
    def visitDivision(self, ctx: funxParser.DivisionContext):
        l = list(ctx.getChildren())
        if self.visit(l[2]) == 0:
            raise ZeroDivisionError("ERRROR: 0 Division")
        else:
            return self.visit(l[0]) / self.visit(l[2])

    # Visit a parse tree produced by funxParser#Power.
    def visitPower(self, ctx: funxParser.PowerContext):
        l = list(ctx.getChildren())
        return pow(self.visit(l[0]), self.visit(l[2]))

    # Visit a parse tree produced by funxParser#Minus.
    def visitMinus(self, ctx: funxParser.MinusContext):
        l = list(ctx.getChildren())
        return -1 * self.visit(l[1])

    # Visit a parse tree produced by funxParser#Modul.
    def visitModul(self, ctx: funxParser.ModulContext):
        l = list(ctx.getChildren())
        return self.visit(l[0]) % self.visit(l[2])

    """
        ------------------------------------------------------------
        VARIABLES  -------------------------------------------------
        ------------------------------------------------------------
        """

    # Visit a parse tree produced by funxParser#Declaration.
    def visitDeclaration(self, ctx: funxParser.DeclarationContext):
        l = list(ctx.getChildren())

        # la funxesio es troba en l[2]
        value = self.visit(l[2])
        self.stack[-1][l[0].getText()] = value
        return None

    # Visit a parse tree produced by funxParser#Variable.
    def visitVariable(self, ctx: funxParser.VariableContext):
        l = list(ctx.getChildren())
        if not l[0].getText() in self.stack[-1]:
            raise NameError(
                "ERROR: " +
                l[0].getText() +
                " is a non declared variable")
        else:
            return self.stack[-1][l[0].getText()]

    """
        ------------------------------------------------------------
        OPERADORS LOGICS -------------------------------------------
        ------------------------------------------------------------
        """

    # Visit a parse tree produced by funxParser#BracketsComparison.
    def visitBracketsComparison(
            self, ctx: funxParser.BracketsComparisonContext):
        l = list(ctx.getChildren())
        return self.visit(l[1])

    # Visit a parse tree produced by funxParser#EqualComparison.
    def visitEqualComparison(self, ctx: funxParser.EqualComparisonContext):
        l = list(ctx.getChildren())
        return int(self.visit(l[0]) == self.visit(l[2]))

    # Visit a parse tree produced by funxParser#LessThanComparison.
    def visitLessThanComparison(
            self, ctx: funxParser.LessThanComparisonContext):
        l = list(ctx.getChildren())
        return int(self.visit(l[0]) < self.visit(l[2]))

    # Visit a parse tree produced by funxParser#GreaterThanComparison.
    def visitGreaterThanComparison(
            self, ctx: funxParser.GreaterThanComparisonContext):
        l = list(ctx.getChildren())
        return int(self.visit(l[0]) > self.visit(l[2]))

    # Visit a parse tree produced by funxParser#LessOrEqualThanComparison.
    def visitLessOrEqualThanComparison(
            self, ctx: funxParser.LessOrEqualThanComparisonContext):
        l = list(ctx.getChildren())
        return int(self.visit(l[0]) <= self.visit(l[2]))

    # Visit a parse tree produced by funxParser#GreaterOrEqualThanComparison.
    def visitGreaterOrEqualThanComparison(
            self, ctx: funxParser.GreaterOrEqualThanComparisonContext):
        l = list(ctx.getChildren())
        return int(self.visit(l[0]) >= self.visit(l[2]))

    # Visit a parse tree produced by funxParser#NotEqualComparison.
    def visitNotEqualComparison(
            self, ctx: funxParser.NotEqualComparisonContext):
        l = list(ctx.getChildren())
        return int(self.visit(l[0]) != self.visit(l[2]))

    # Visit a parse tree produced by funxParser#logicAnd.
    def visitLogicAnd(self, ctx: funxParser.LogicAndContext):
        l = list(ctx.getChildren())
        left = self.visit(l[0])
        right = self.visit(l[2])
        return int(left and right)

    # Visit a parse tree produced by funxParser#logicOr.
    def visitLogicOr(self, ctx: funxParser.LogicOrContext):
        l = list(ctx.getChildren())
        left = self.visit(l[0])
        right = self.visit(l[2])
        return int(left or right)

    # Visit a parse tree produced by funxParser#Not.
    def visitNot(self, ctx: funxParser.NotContext):
        l = list(ctx.getChildren())
        return int(not self.visit(l[1]))

    # Visit a parse tree produced by funxParser#True.
    def visitTrue(self, ctx: funxParser.TrueContext):
        return 1

    # Visit a parse tree produced by funxParser#False.
    def visitFalse(self, ctx: funxParser.FalseContext):
        return 0

    """
        ------------------------------------------------------------
        CONDICIONALS  ----------------------------------------------
        ------------------------------------------------------------
        """

    # Visit a parse tree produced by funxParser#IfThen.
    def visitIfThen(self, ctx: funxParser.IfThenContext):
        l = list(ctx.getChildren())
        # per defecte el resultat es None
        result = None
        # obte el resultat d'avaluar la condicio
        conditionResult = self.visit(l[1])

        if conditionResult:
            i = 3   # index de la primera instruccio
            while l[i].getText() != '}' and result is None:
                result = self.visit(l[i])
                i += 1
        return result

    # Visit a parse tree produced by funxParser#IfThenElse.
    def visitIfThenElse(self, ctx: funxParser.IfThenElseContext):
        l = list(ctx.getChildren())

        # per defecte el resultat es None
        result = None
        # obte el resultat d'avaluar la condicio
        conditionResult = self.visit(l[1])

        if conditionResult:
            i = 3   # index de la primera instruccio del if
            while l[i].getText() != '}' and result is None:
                result = self.visit(l[i])
                i += 1
        else:
            i = 5  # index de la primera instruccio del else
            while l[i].getText() != '}' and result is None:
                result = self.visit(l[i])
                i += 1
        return result

    """
        ------------------------------------------------------------
        BUCLES -----------------------------------------------------
        ------------------------------------------------------------
        """

    # Visit a parse tree produced by funxParser#while.
    def visitWhile(self, ctx: funxParser.WhileContext):
        l = list(ctx.getChildren())
        # per defecte el resultat es None
        result = None

        while self.visit(l[1]):
            i = 3
            while l[i].getText() != '}' and result is None:
                result = self.visit(l[i])
                i += 1
        return result

    # Visit a parse tree produced by funxParser#for.
    def visitFor(self, ctx: funxParser.ForContext):
        l = list(ctx.getChildren())

        # per defecte el resultat es None
        result = None

        # inicialitzacio del bucle
        self.visit(l[1])

        # bucle
        while (self.visit(l[3])):
            i = 7           # index de la primera instruccio del bucle
            while l[i].getText() != '}' and result is None:
                result = self.visit(l[i])
                i += 1
            # augment/decrement de l'iterador
            self.visit(l[5])
        return result

    """
        ------------------------------------------------------------
        FUNCIONS ---------------------------------------------------
        ------------------------------------------------------------
        """

    # Visit a parse tree produced by funxParser#Function.
    def visitFunction(self, ctx: funxParser.FunctionContext):
        l = list(ctx.getChildren())
        name = l[0].getText()

        # comprova si la funcio ja ha estat definida
        if name in self.procedures:
            raise NameError(
                "ERROR: Procedure " +
                l[0].getText() +
                " already defined")

        # llegeix els parametres de la funcio
        i = 1
        params = []
        while l[i].getText() != '{':
            params.append(l[i].getText())
            i += 1

        # comprova que no hi hagi identificadors repetits
        if len(params) != len(set(params)):
            raise AttributeError(
                "ERROR: Repeated arguments in procedure declaration")

        # crea un objecte de tipus procedure, amb el nom de la funcio
        # els parametres i el seu bloc de codi
        self.procedures[name] = Procedure(name, params, ctx)
        self.procedures_params.append(name + ' ' + ' '.join(params))
        return

    # Visit a parse tree produced by funxParser#FunctionCall.
    def visitFunctionCall(self, ctx: funxParser.FunctionCallContext):
        l = list(ctx.getChildren())
        name = l[0].getText()

        # comprova que el procediment estigui definit
        if name not in self.procedures:
            raise NameError("ERROR: procedure " + name + "() is not defined")

        # obte els valors dels parametres
        paramValues = []
        for i in range(1, len(l)):
            paramValues.append(self.visit(l[i]))

        return self.executeProcedure(name, paramValues)

    # funcio que s'encarrega d'executar un procediments
    def executeProcedure(self, name, paramValues):
        # comprova que el numero de parametres sigui el correcte
        if len(self.procedures[name].params) != len(paramValues):
            raise AttributeError(
                "ERROR: incorrect number of arguments in procedure " +
                name +
                "()")

        # inicialitza el diccionari ambs els parells de variables <nom
        # variable, valor>
        variables = {}

        # asigna els parametres a les variables de la funcio
        for param, value in zip(self.procedures[name].params, paramValues):
            variables[param] = value

        # afegeix un nou bloc a la pila, que representa el nou context introduit per la funcio
        # que tindra les seves respectives variables

        self.stack.append(variables)
        l = list(self.procedures[name].context.getChildren())
        i = 0
        while l[i].getText() != '{':
            i += 1
        i += 1            # l'index esta ara a la primera linea de codi de la funcio

        # per defecte el resultat es None
        result = None

        while l[i].getText() != '}' and result is None:
            result = self.visit(l[i])
            i += 1
        # un cop executada la funcio, elimina el seu bloc del stack
        self.stack.pop(-1)
        return result

    # metode per enviar a l'aplicació web els noms i paràmetres dels
    # procediments
    def getProceduresParams(self):
        return self.procedures_params


"""
PART DE L'APICACIO WEB ---------------------------------------------------------------
"""

app = Flask(__name__)
if __name__ == "__main__":
    app.run()

historial = []
evaluator = funx()
historial_procedures = []


@app.route("/")
def index():
    return render_template("base.html")


@app.route('/read', methods=['POST'])
def leer():
    # contingut de la consola en l'aplicacio web
    input = request.form.get("console")
    input_stream = InputStream(input)

    try:
        # se la pasa al lexer, que la tokeniza
        lexer = funxLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        # el parser construye el AST a partir de los tokens
        parser = funxParser(token_stream)
        tree = parser.root()
        # y se pasa el AST al Tree Visitor
        output = evaluator.visit(tree)
    except NameError as ne:
        output = ne
    except AttributeError as ae:
        output = ae
    except ZeroDivisionError as ze:
        output = ze

    index = int(len(historial) / 2) + 1
    historial.append("In " + str(index) + ":" + input)
    historial.append("Out " + str(index) + ":" + str(output))
    lastFive = historial[-10:]

    # obte els procediments i els seus respectius parametres creats fins ara
    historial_procedures = evaluator.getProceduresParams()

    # recarga la página
    return render_template(
        "base.html",
        lastFive=lastFive,
        historial_procedures=historial_procedures)
