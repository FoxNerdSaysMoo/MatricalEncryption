# Once the encryption system is working, this will be a example of its usage
from connection import ArrayEncryptor
import sanic


app = sanic.Sanic(__name__)
fail = sanic.response.html('<h1>So close... But so far.</h1>')

@app.route('/')
def main(request):
    print(request.args)

    if not request.args:
        print('No json :: Failure')
        return fail

    if 'dims' not in request.args:
        print('Dims not in json :: Failure')
        return fail
    
    return sanic.response.html('<h1>Congrats!</h1>')

app.run(host="0.0.0.0", port=8000)
