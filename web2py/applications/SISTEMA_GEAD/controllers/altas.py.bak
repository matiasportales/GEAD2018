# coding: utf8
# intente algo como
def index(): return dict(message="hello from admin.py")

# coding: utf8
# intente algo como
#def admin():
#    grid = SQLFORM.grid(db.socios)
#    return dict(grid=grid)

def altas_socios():
    form = SQLFORM(db.socios,submit_button='Aceptar')
    if form.accepts(request.vars, session):
        response.flash = 'NUEVO SOCIO INGRESADO'
#        redirect(URL('dar_permiso'))
    elif form.errors:
        response.flash = 'HAY ERRORES EN EL INGRESO'
    else:
        response.flash = 'POR FAVOR COMPLETE EL FORMULARIO'    
    return dict(form=form)
