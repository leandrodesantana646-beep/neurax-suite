<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neurax - Cobrança Pix</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }
        body {
            background-color: #f4f6f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 20px;
        }
        .neurax-container {
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 400px;
        }
        h2 {
            color: #333333;
            font-size: 20px;
            margin-bottom: 15px;
            text-align: center;
        }
        .input-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            font-size: 14px;
            color: #333333;
            margin-bottom: 5px;
            font-weight: bold;
        }
        /* CAMPO DE TEXTO COM LETRA PRETA GARANTIDA */
        input {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            color: #000000 !important;
            background-color: #ffffff !important;
            border: 1px solid #cccccc;
            border-radius: 8px;
            outline: none;
        }
        input::placeholder {
            color: #888888;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #4f46e5;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }
        button:active {
            background-color: #4338ca;
        }
    </style>
</head>
<body>

    <div class="neurax-container">
        <h2>Neurax - Gerar Pix</h2>
        
        <div class="input-group">
            <label for="descricao">Descrição do Produto</label>
            <input type="text" id="descricao" placeholder="Ex: Consultoria">
        </div>

        <div class="input-group">
            <label for="valor">Valor (R$)</label>
            <input type="text" id="valor" placeholder="Ex: 150.00">
        </div>

        <div class="input-group">
            <label for="nome">Nome do Cliente</label>
            <input type="text" id="nome" placeholder="Ex: João Silva">
        </div>

        <button onclick="alert('Dados prontos para enviar ao Make!')">Gerar Cobrança</button>
    </div>

</body>
</html>
