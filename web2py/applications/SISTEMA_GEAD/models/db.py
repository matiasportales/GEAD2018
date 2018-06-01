# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()


db.define_table(
    auth.settings.table_user_name,
    Field('id_socio','string',default='',readable = False, writable = False),
    Field('first_name','string',requires = IS_UPPER(),length=64, default='',label=T('Nombre')),
    Field('last_name','string',requires = IS_UPPER(),length=64, default='',label=T('Apellido')),
    Field("dni",'integer',label=T('DNI')),
    Field('password','password', length=64,readable=False, label=('Contraseña')),
    Field('email','string', length=64, default='',label=T('E-Mail')),
    Field("domicilio",'string',requires = IS_UPPER(),label=T('Domicilio')),
    Field("localidad",'string',requires = IS_UPPER(),label=T('Localidad')),
    Field("cp",'integer',length=4, label=T('Codigo Postal')),
    Field("telefono1",'string',label=T('Telefono')),
    Field("telefono2",'string',label=T('Telefono 2')),
    Field('registration_key', length=64,
          writable=False, readable=False, default='',label=T('Clave de registracion')),
    Field('reset_password_key', length=64,
          writable=False, readable=False, default='',label=T('Clave de contraseña de restablecimiento')),
    Field('registration_id', length=64,
          writable=False, readable=False, default='',label=T('ID de registracion'))
          )


## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
###################################################




db.define_table('actividad',
    Field ('fecha', 'date',default = request.now, readable = True, writable = False),
    Field ('id_actividad', 'id'),
    Field ('foto', type='upload', length=50),
    Field ('nombre_actividad','string'),
    #Field ('horarioydia_actividad','datetime',label=T("Hora y dia actividad")),
    Field ('descripcion','text',label=T('Descripcion')),
    #Field ('precio_cuota','double'),
    auth.signature,
    format='%(nombre_actividad)s')


db.actividad.nombre_actividad.requires= IS_NOT_EMPTY(error_message='No se ingreso nombre de la actividad.') 
#db.actividad.horarioydia_actividad.requires= IS_NOT_EMPTY(error_message='No se ingreso horario y dia de la actividad.')
db.actividad.foto.requires= IS_NOT_EMPTY(error_message='No se subio ninguna foto.')


db.define_table('socios',
    Field ('fecha','date',default = request.now, readable = True, writable = False),
    Field ('id_actividad',db.actividad,label=T('Actividad')),
    Field ('id_socio','id'),
    Field ('foto', type='upload', length=50),
    Field ('nombre_socio', type='string', length=200),
    Field ('apellido_socio', 'string'),
    Field ('dni_socio', type='integer'),
    Field ('fecha_nacimiento', type='date'),
    Field ('direccion', type='string', length=200),
    Field ('localidad', type='string', length=50),
    Field ('cp', type='string', length=7),
    Field ('telefono_fijo','integer',length=8),
    Field ('telefono_movil','integer',length=12),
    Field ('genero','string',requires = IS_IN_SET(['Masculino','Femenino'])),
    Field ('mail','string',unique = True,requires = IS_EMAIL()),
    format='%(dni_socio)s')

db.socios.foto.requires= IS_NOT_EMPTY(error_message='No se subio ninguna foto.')
db.socios.nombre_socio.requires= IS_NOT_EMPTY(error_message='No se ingreso ningun nombre.')
db.socios.apellido_socio.requires= IS_NOT_EMPTY(error_message='No se ingreso ningun apellido')
#db.socios.fecha_nacimiento.requires= IS_NOT_EMPTY(error_message='No se ingreso ninguna fecha.')
db.socios.dni_socio.requires= IS_NOT_IN_DB(db,'socios.dni_socio')
db.socios.direccion.requires= IS_NOT_EMPTY(error_message='No se ingreso ninguna dirección.')
db.socios.localidad.requires= IS_NOT_EMPTY(error_message='No se ingreso ninguna localidad.')
db.socios.cp.requires= IS_NOT_EMPTY(error_message='No se ingreso ningun codigo postal.')
db.socios.telefono_fijo.requires= IS_NOT_EMPTY(error_message='No se ingreso ningun telefono fijo.')
db.socios.telefono_movil.requires= IS_NOT_EMPTY(error_message='No se ingreso ningun telefono móvil.')
db.socios.genero.requires= IS_IN_SET(('Masculino','Femenino'))
db.socios.mail.requires= IS_NOT_EMPTY(error_message='No se ingreso ningun mail.')




db.define_table('pago',
    Field ('id_socio',db.socios ,label=T('Socios')),
    Field ('id_pago', 'id'),
    Field ('fecha_pago','date'),
    Field ('mes_abonado','string',requires = IS_IN_SET(['Enero','febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']))
               ),

#db.pago.mes_pago.requires=IS_IN_SET('Enero','febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre')

db.define_table('factura',
    Field ('id_socio', db.socios ),
    Field ('n_factura', 'id'),
    Field ('fecha', 'date', default = request.now, readable = True, writable = True),
    Field ('id_pago',db.pago),
    Field('total','double')),



db.define_table('pagos_pendientes',
    Field ('id_pago', db.pago),
    Field ('id_socio', db.socios),    
    #Field ('fecha_pago', db.pago),
   # Field ('mes_pago', db.pago)
          ),
