from helpers.application import app
from controllers.instituicaoEnsinoControler import instituicaoEnsino_bp

app.register_blueprint(instituicaoEnsino_bp)

# TODO: ROTAS E METODOS
def main(arg=[]):
    app.run(debug=True)

if __name__ == "__main__":
    main()