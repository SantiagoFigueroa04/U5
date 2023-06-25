from flask import render_template
from flask import Flask,request,url_for,redirect,session,flash
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib



app=Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Curso,Estudiante,Preceptor,Asistencia

@app.route('/')
def bienvenido():
    return render_template('bienvenida.html')

@app.route('/inicio_sesion')
def inicio_sesion():
    return render_template('inicio.html')

@app.route('/verificacion',methods= ['POST','GET'])
def verificacion():
    email=request.form['correo']
    clave=request.form['contrasena']
    clavecifrada=hashlib.md5(clave.encode()).hexdigest()
    if not email and not clave:
        return render_template('bienvenida.html')
    usuario = Preceptor.query.filter_by(correo=email, clave=clavecifrada).first()
    if usuario:
        session["preceptor"] = email
        return redirect(url_for('pagina_preceptor',correo = email))
    else:
        flash('Correo o contraseña incorrectos', 'error')
        return render_template('inicio.html')

@app.route('/preceptor',methods =['POST','GET'] )
def pagina_preceptor():
    email = request.form.get('correo')
    correo_preceptor = session.get("preceptor")
    usuario = Preceptor.query.filter_by(correo=correo_preceptor).first()
    return render_template('paginapreceptor.html',correo=correo_preceptor, nombre=usuario.nombre, apellido=usuario.apellido)

@app.route('/registrar_asistencia')
def registrar_asistencia():
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    cursos = Curso.query.filter_by(idpreceptor=preceptor.id).all()
    return render_template('cursoclase.html', cursos=cursos, preceptor=preceptor)


@app.route('/asistencia_curso',methods=['POST','GET'])
def asistencia_curso():
    idpreceptor=request.args.get('idpreceptor')
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    idcurso=request.form.get('cursos')
    curso = Curso.query.filter_by(id=idcurso).first()
    alumnos=Estudiante.query.all()
    return render_template('asistencia_curso.html', curso=curso, alumnos=alumnos,preceptor=preceptor)

@app.route('/asistencia_alumno', methods=['GET'])
def asistencia_alumno():
    idcurso = request.args.get('idcurso')
    tipoclase = request.args.get('clase')
    fecha = request.args.get('fecha')
    idalumno = request.args.get('alumno')
    alumno = Estudiante.query.filter_by(id=idalumno).first()
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    idpreceptor = preceptor.id
    return render_template('confirmar_asistencia.html', tipoclase=tipoclase, fecha=fecha, alumno=alumno, idcurso=idcurso, idalumno=idalumno,preceptor=idpreceptor)


@app.route('/confirmar_asistencia', methods=['POST'])
def confirmar_asistencia():
    idcurso = request.args.get('idcurso')
    asistencia = Asistencia(fecha=request.form['fecha'], codigoclase=request.form['tipoclase'], asistio=request.form['asis'], justificacion=request.form['justificacion'], idestudiante=request.form.get('idalumno'))
    db.session.add(asistencia)
    db.session.commit()
    cursos=Curso.query.all()
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    return redirect(url_for('registrar_asistencia', cursos=cursos,preceptor=preceptor))
    
@app.route('/listar_asistencia')
def listar_asistencia():
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    cursos = Curso.query.filter_by(idpreceptor=preceptor.id).all()
    return render_template('funcionalidad3.html', cursos=cursos, preceptor=preceptor)

@app.route('/informe',methods=['POST','GET'])
def informe():
    idcurso=request.form.get('cursos')
    curso = Curso.query.filter_by(id=idcurso).first()
    alumnos = Estudiante.query.all()
    asistencia=Asistencia.query.all()
    correo_preceptor = session.get("preceptor")
    preceptor = Preceptor.query.filter_by(correo=correo_preceptor).first()
    return render_template('listar.html', curso=curso, alumnos=alumnos,asistencia=asistencia,preceptor=preceptor)


if __name__=='__main__':
    
    app.run(debug=True)