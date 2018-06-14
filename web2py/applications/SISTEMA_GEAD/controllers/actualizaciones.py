# coding: utf8
# intente algo como
def index(): return dict(message="hello from actualizaciones.py")

def listar_socios():
    if(request.get_vars.buscar):
        soc = db((db.socios.dni_socio.like('%'+request.get_vars.buscar+'%'))).select()
    try:
        soc
    except:
        soc = db().select(db.socios.ALL)
    return dict(soc=soc)

def modificar_socios():
    soc = db(db.socios.dni_socio==request.args(0)).select()
    socio = soc[0]
    form = SQLFORM(db.socios,socio,deletable=False,
           Field=['id_socio','nombre_socio','dni_socio','foto','apellido_socio','direccion','localidad','cp','fecha_nacimiento','telefono_movil','telefono_fijo','mail'],
           labels = {'id_socio':'NRO DE SOCIO','nombre_socio':'NOMBRE','foto':'FOTO','dni_socio':'DNI','apellido_socio':'APELLIDO','direccion':'DOMICILIO','localidad':'LOCALIDAD',
                                'cp':'CODIGO POSTAL','contacto':'CONTACTO','telefono_movil':'TELEFONO MOVIL','telefono_fijo':'TELEFONO FIJO','mail':'MAIL'},
                                submit_button='Grabar')
    response.flash="ADVERTENCIA:Los datos modificados se guardaran en la base de datos"
    if form.accepts(request.vars, session):
        response.flash = 'Los datos fueron modifiados'
        redirect(URL(r=request,f='listar_socios'))
    return dict(form=form)

def socios():
    if(request.get_vars.buscar):
        soc = db((db.socios.dni_socio.like('%'+request.get_vars.buscar+'%'))).select()
    try:
        soc
    except:
        soc = db().select(db.socios.ALL)
    return dict(soc=soc)
