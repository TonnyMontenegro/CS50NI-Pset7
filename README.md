# Problem Set 7: C$50 Finance

1.  Implementa <a href="#C$50 Finance" class="btn btn-sm btn-default">C$50 Finance</a>

### Entendiendo

#### `application.py`

Abre  `application.py`. En la parte superior hay un grupo de imports, entre ellos, el módulo SQL de CS50 y unas cuantas funciones de ayuda. Nos enfocaremos en eso luego.

Luego de configurar  [Flask](http://flask.pocoo.org/), notaras como este archivo deshabilita el cacheo de respuestas (ya que estas en el modo depuración, conocido también como servidor de desarrollo, habilitado por defecto en el IDE CS50), lo que te permite realizar cualquier cambio sin necesidad de reiniciar el servidor. También, notaras como configura a  [Jinja](http://jinja.pocoo.org/)  con un filtro personalizado,  `usd`, una función definida en  `helpers.py`  que hará más fácil formatear los valores a dólares. También se configura a flask para que pueda manejar  [sesiones](http://flask.pocoo.org/docs/0.12/quickstart/#sessions)  en el sistema de archivos local (el disco), y no en cookies, lo que es predeterminado en flask. El archivo configura al módulo SQL de CS50 a usar  `finance.db`, una base de datos SQLite que veremos a más adelante.

Luego, hay un conjunto de rutas, de las cuales, solo dos están completamente implementadas:  `login`  y  `logout`. Revisa la implementación de  `login`  primero. Veras como usa a  `db.execute`  (de la librería de CS50) para consultar a  `finance.db`; y también veras como utiliza un  `check_password_hash`  para verificar las contraseñas ingresadas. Finalmente, notaras como  `login`  “recuerda” que un usuario tiene una sesión activa almacenando su  `user_id`, un entero en  `session`. De esa manera, todas las demás rutas podrán sabes que usuario está en sesión, si es que hay uno. De igual manera, revisa como es que  `logout`  simplemente vacía los valores en  `session`  para cerrar la sesión.

Observa como muchas rutas están “decoradas” con  `@login_required`  (una función definida en  `helpers.py`). Ese decorador se asegura de que, si un usuario intenta entrar a alguna de esas rutas, será redireccionado a  `login`  para iniciar sesión.

Observa también, que muchas rutas soportan GET y POST. Aunque, por ahora solo retornen una disculpa, ya que no están implementadas, todavía.

#### `helpers.py`

Ahora, dale un vistazo a  `helpers.py`, aquí hay una implementación de  `apology`. Observa como renderiza una plantilla,  `apology`.html. Dentro de apology, está definida la función  `escape`, que ayuda un poco con los caracteres especiales. Esta función está dentro de  `apology`  ya que solo esta lo requiere.

Lo siguiente es  `login_required`. No te preocupes si no lo entiendes, pero si alguna vez te has preguntado como una función puede retornar otra función, aquí esta la respuesta.

Mas adelante, esta  `lookup`, una función a la cual dado un  `símbolo`  (por ejemplo NFLX), retorna los detalles de la acción de ese símbolo en forma de un  `diccionario`  con tres claves:  `name`, cuyo valor es un  `str`  (por ejemplo “Netflix Inc.”);  `price`, cuyo valor es un  `float`, y  `symbol`, cuyo valor es un  `str`, el propio símbolo de la empresa completamente en mayúsculas, sin importar si cuando dicho símbolo fue dado a la función iba en mayúsculas o minúsculas.

Finalmente, tenemos a  `usd`, una función corta que da formato a un  `float`  como un dólar americano (por ejemplo 1234.56 retornará como $1,234.56).

#### `requirements.txt`

Este archivo solo contiene los paquetes que son dependencias de esta aplicación.

#### `static/`

Revisa también esta carpeta, dentro de la cual esta  `styles.css`, que contiene unos estilos predeterminados. Eres libre de agregar otros estilos si gustas.

#### `templates/`

Ahora revisa  `templates/`. En  `login.html`  se contiene un formulario HTML, estilizado con  [Bootstrap](http://getbootstrap.com/). En  `apology.html`, hay una plantilla para una disculpa. Recuerda que  `apology`  en  `helpers.py`  toma dos argumentos:  `message`, que es pasado a  `render_template`  como el valor de  `bottom`, y opcionalmente,  `code`, que es pasado al valor de  `top`. Mira como en  `apology.html`  son utilizados estos valores, y aquí está el  [por qué](https://github.com/jacebrowning/memegen)  0:-).

Finalmente estará  `layout.html`. Es el más grande de todos, pero lo es principalmente porque integra una muy bonita barra de navegación apta para los móviles, también sacada de Bootstrap. Observa como esta define a un bloque,  `main`, dentro del cual las demás plantillas (incluida  `apology.html`  y  `login.html`) se insertan. También incluye el  [message flashing](https://flask.palletsprojects.com/en/1.1.x/), lo que te permite mover mensajes de una ruta a otra para ser vistos por el usuario.

## Especificación

### `register`

Completar la implementación de  `register`, para permitir al usuario registrarse en el sitio creando una cuenta

-   Requerir el ingreso de un nombre de usuario, mediante un campo de texto cuyo  `name`  es  `username`. Renderizar una disculpa en caso de que no se ingrese un nombre de usuario o si el nombre del usuario ya está en uso.
    
-   Requerir el ingreso de una contraseña, mediante un campo de texto cuyo  `name`  es  `password`, y luego, pedir que se confirme (ingresando de nuevo la misma) la contraseña en un campo cuyo  `name`  es  `confirmation`. Renderizar una disculpa en caso de que no se ingrese una contraseña, o si las contraseñas no coinciden.
    
-   Hacer envió del formulario mediante  `POST`  a  `/register`.
    
-   `INSERTAR`  el usuario nuevo en  `users`, almacenando un hash de la contraseña ingresada y no la contraseña en sí. Puedes hacer el hash mediante  [`generate_password_hash`](http://werkzeug.palletsprojects.com/en/0.16.x/utils/#module-werkzeug.security).
    
-   Lo mas probable es que necesites una plantilla para esta acción (`register.html`), la cual es similar a  `login.html`.
    

Una vez que hayas implementado  `register`  correctamente, debes ser capaz de registrar una cuenta en el sitio e iniciar sesión con la misma (siempre y cuanto  `login`  y  `logout`  sean funcionales). Y debes ser capaz de ver estos nuevos registros en phpLiteAdmin o  `sqlite3`.

### `quote`

Completa la implementación de  `quote`, tal que permita al usuario cotizar los precios actuales de las acciones.

-   Requerir al usuario el ingreso del símbolo de la empresa, en un campo cuyo  `name`  es  `symbol`.
    
-   Ingresar el formulario mediante  `POST`  a  `/quote`.
    
-   Lo mas probable es que quieras crear un par de plantillas nuevas (`quote.html`  y  `quoted.html`). Cuando un usuario visite  `/quote`  mediante GET, renderizar una de estas plantillas que sea capaz de buscar en  `/quote`  mediante POST. En respuesta a POST,  `quote`  deberá renderizar la segunda plantilla, agregándole uno o más valores desde  `lookup`.
    

### `buy`

Completa la implementación de  `buy`, para que permita a un usuario comprar acciones.

-   Requerir que el usuario ingrese el símbolo de la empresa en bolsa, mediante un campo cuyo  `name`  es  `symbol`. Renderizar una disculpa en caso de que no se ingrese o el símbolo no se encuentre.
    
-   Requerir que el usuario ingrese un numero de títulos, implementado mediante un campo cuyo  `name`  es  `shares`, Renderizar una disculpa en caso de que el ingreso del usuario no sea un entero positivo.
    
-   Enviar el formulario mediante  `POST`  a  `/buy`.
    
-   Quizá quieras usar a  `lookup`  para verificar el precio de la acción
    
-   Quizá quieras hacer  `SELECT`  para ver de cuanto dinero dispone el  `usuario`  en su cuenta en users.
    
-   Añadir una o mas tablas nuevas a  `finance.db`  por las cuales puedas llevar registros de las compras hechas. Almacena la información necesaria para saber quién compro, a qué precio y cuando.
    
    -   Usa los tipos apropiados de SQLite
        
    -   Define índices  `UNIQUE`  en todos los campos que crees que deben ser únicos
        
    -   Define índices non-`UNIQUE`  en cualquier campo donde vayas a buscar (mediante  `SELECT`  y  `WHERE`).
        
    
-   Renderiza una disculpa sin concretar la compra, si el usuario no tiene suficiente dinero para realizar su compra.
    
-   No necesitas preocuparte en caso de condiciones de carrera (o puedes usar transacciones).
    

Una vez que hayas implementado  `buy`  correctamente, debes poder ver las compras hechas mediante phpLiteAdmin o  `sqlite3`.

### `index`

Completa la implementación de  `index`, para poder mostrar en una tabla HTML, en forma de resumen, todas las acciones, títulos y precios de lo que el usuario actual posee, y el valor total de cada holding (títulos por precio). También muestra al usuario el balance de efectivo total, y un gran total (valor total de acciones más efectivo).

-   Quizá quieras ejecutar múltiples  `SELECT`s. En dependencia de como implementes tus tablas, puede ser que necesites  [GROUP BY](https://www.google.com/search?q=SQLite+GROUP+BY),  [HAVING](https://www.google.com/search?q=SQLite+HAVING),  [SUM](https://www.google.com/search?q=SQLite+SUM), y/o  [WHERE](https://www.google.com/search?q=SQLite+WHERE).
    
-   Puede que quieras usar a  `lookup`  para cada acción.
    

### `sell`

Completa la implementación de  `sell`, de tal forma que permita a los usuarios vender las acciones que posean.

-   Requerir que el usuario ingrese el símbolo de una empresa en bolsa, mediante un menú de selección cuyo  `name`  es  `symbol`. Renderizar una disculpa en caso de que no se seleccione correctamente o si el usuario no posee títulos de esa acción.
    
-   Requerir que el usuario ingrese el numero de títulos a vender, implementado mediante un campo de texto cuyo  `name`  es  `shares`. Renderizar una disculpa en caso de que no se ingrese un entero positivo o si el usuario no posee ese numero de títulos de acciones.
    
-   Enviar el formulario mediante  `POST`  a  `/sell`
    
-   No necesitas preocuparte en caso de condiciones de carrera (o puedes usar transacciones).
    

### `history`

Completa la implementación de  `history`, para que muestre una tabla HTML, haciendo un registro de todas las transacciones hechas por el usuario, mostrando fila por fila, cada compra o venta.

-   Para cada fila, asegúrate de mostrar claramente los detalles de la transacción (símbolo, precio, numero de títulos, y hora y fecha de la transacción)
    
-   Quizá necesites modificar la tabla que creaste para  `buy`  o utilizar una tabla adicional, trata de minimizar las redundancias.
    

### Toque personal

Implementa al menos un toque personal de tu elección:

-   Permitir a los usuarios cambiar su contraseña.
    
-   Permitir a los usuarios agregar efectivo adicional.
    
-   Permitir a los usuario la compra o ventas de títulos directamente desde  `index`, sin necesidad de buscarlos manualmente.
    
-   Requerir que las contraseñas tengan letras, números y/o símbolos
    
-   Implementar otra característica de un alcance comparable.