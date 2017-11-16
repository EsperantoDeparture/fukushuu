from django.shortcuts import render
from .forms import CodigoFuente
from django.template.context_processors import csrf
from .fukushuu.main import main as compilador
from .fukushuu.excepciones import ExceptionFound
from antlr4 import RecognitionException, NoViableAltException, IllegalStateException


# Create your views here.
def compilar(request):
    form = CodigoFuente()
    if request.method == 'POST':
        err = False
        try:
            salida = compilador(request.POST["codigo"]).split("\n")
        except NoViableAltException as e:
            salida = [str(e)]
            err = True
        except IllegalStateException as e:
            salida = [str(e)]
            err = True
        except RecognitionException as e:
            salida = [str(e)]
            err = True
        except ExceptionFound as e:
            salida = [str(e)]
            err = True
        return render(request, 'inicio.html', {"has_form": False, "salida": salida, "err": err})
    else:
        args = {"has_form": True, "ruta": "/inicio/", "form": form}
        args.update(csrf(request))

        return render(request, 'inicio.html', args)
