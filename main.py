import db.matrices as mat

def data_load():
    mat.crear_usuario("tomiicotos", "tomi", "admin")
    mat.crear_usuario("crisvlasova", "cris", "admin")
    mat.crear_usuario("thiagocaimer", "thiago")

def run():
    data_load()

if __name__ == "__main__":
    run()