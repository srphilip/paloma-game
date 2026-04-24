import streamlit as st
import streamlit.components.v1 as components
import base64
from PIL import Image, ImageOps
import io

st.set_page_config(layout="wide", page_title="Circuito de Quebra-Cabeça SESI")

# --- ÁREA DE UPLOAD (Para gerar as strings Base64 das suas 4 fotos) ---
st.title("🧩 Circuito de Quebra-Cabeça - 4 Fases")
st.write("Suba as 4 fotos para gerar o jogo automático.")

ficheros = st.file_uploader("Selecione as 4 fotos de uma vez", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if len(ficheros) >= 4:
    lista_base64 = []
    for f in ficheros[:4]:
        img = Image.open(f)
        img = ImageOps.fit(img, (500, 500), Image.Resampling.LANCZOS)
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        lista_base64.append(f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode()}")

    # --- O JOGO EM HTML PURO ---
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; background: #e0e7ff; margin: 0; padding: 20px; touch-action: manipulation; }}
            h2 {{ color: #1e3a8a; margin-bottom: 10px; }}
            
            #puzzle-board {{
                display: grid;
                grid-template-columns: repeat(2, 200px);
                grid-template-rows: repeat(2, 200px);
                gap: 8px;
                background: #ffffff;
                padding: 10px;
                border: 8px solid #1e3a8a;
                border-radius: 15px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            }}

            .slot {{
                width: 200px;
                height: 200px;
                background: #f1f5f9;
                border: 2px dashed #cbd5e1;
                border-radius: 8px;
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            #pieces-container {{
                display: flex;
                gap: 15px;
                margin-top: 30px;
                min-height: 160px;
                padding: 20px;
                background: #ffffffaa;
                border-radius: 20px;
                flex-wrap: wrap;
                justify-content: center;
                width: 90%;
            }}

            .piece {{
                width: 140px;
                height: 140px;
                background-size: 280px 280px;
                cursor: grab;
                border: 3px solid #fff;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }}

            /* Modal de Vitória */
            #modal-vitoria {{
                display: none;
                position: fixed;
                top: 50%; left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                padding: 40px;
                border-radius: 30px;
                box-shadow: 0 0 100px rgba(0,0,0,0.3);
                text-align: center;
                z-index: 1000;
                border: 6px solid #22c55e;
            }}

            button {{
                background: #22c55e;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 20px;
                border-radius: 50px;
                cursor: pointer;
                font-weight: bold;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>

    <h2 id="titulo-fase">Fase 1 de 4</h2>

    <div id="puzzle-board">
        <div class="slot" id="s0" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
        <div class="slot" id="s1" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
        <div class="slot" id="s2" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
        <div class="slot" id="s3" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
    </div>

    <div id="pieces-container">
        <div class="piece" id="p0" draggable="true" ondragstart="drag(event)"></div>
        <div class="piece" id="p1" draggable="true" ondragstart="drag(event)"></div>
        <div class="piece" id="p2" draggable="true" ondragstart="drag(event)"></div>
        <div class="piece" id="p3" draggable="true" ondragstart="drag(event)"></div>
    </div>

    <div id="modal-vitoria">
        <h1 id="msg-vitoria">INCRÍVEL! ✨</h1>
        <p id="msg-sub">Você completou esta foto!</p>
        <button id="btn-proximo" onclick="proximaFase()">PRÓXIMA FASE ➔</button>
    </div>

    <script>
        const fotos = {lista_base64};
        let faseAtual = 0;
        let encaixadas = 0;

        function carregarFase() {{
            encaixadas = 0;
            document.getElementById("titulo-fase").innerText = "Fase " + (faseAtual + 1) + " de 4";
            document.getElementById("modal-vitoria").style.display = "none";
            
            // Limpa slots e move peças de volta para o container
            const container = document.getElementById("pieces-container");
            for(let i=0; i<4; i++) {{
                const p = document.getElementById("p" + i);
                const s = document.getElementById("s" + i);
                s.innerHTML = "";
                
                // Configura a nova imagem
                p.style.backgroundImage = "url('" + fotos[faseAtual] + "')";
                p.style.width = "140px";
                p.style.height = "140px";
                p.style.backgroundSize = "280px 280px";
                p.draggable = true;
                
                // Define posições do background
                if(i===0) p.style.backgroundPosition = "0 0";
                if(i===1) p.style.backgroundPosition = "-140px 0";
                if(i===2) p.style.backgroundPosition = "0 -140px";
                if(i===3) p.style.backgroundPosition = "-140px -140px";
                
                container.appendChild(p);
            }}
            // Embaralha visualmente as peças no container
            for (let i = container.children.length; i >= 0; i--) {{
                container.appendChild(container.children[Math.random() * i | 0]);
            }}
        }}

        function allowDrop(ev) {{ ev.preventDefault(); }}

        function drag(ev) {{
            ev.dataTransfer.setData("text", ev.target.id);
        }}

        function drop(ev) {{
            ev.preventDefault();
            const data = ev.dataTransfer.getData("text");
            const piece = document.getElementById(data);
            const slot = ev.target;

            // Validação rígida: s0 aceita p0, s1 aceita p1...
            if (slot.id === "s" + data.substring(1) && slot.classList.contains("slot")) {{
                piece.style.width = "200px";
                piece.style.height = "200px";
                piece.style.backgroundSize = "400px 400px";
                
                if(data === "p0") piece.style.backgroundPosition = "0 0";
                if(data === "p1") piece.style.backgroundPosition = "-200px 0";
                if(data === "p2") piece.style.backgroundPosition = "0 -200px";
                if(data === "p3") piece.style.backgroundPosition = "-200px -200px";

                slot.appendChild(piece);
                piece.draggable = false;
                encaixadas++;

                if (encaixadas === 4) {{
                    document.getElementById("modal-vitoria").style.display = "block";
                    if(faseAtual === 3) {{
                        document.getElementById("msg-vitoria").innerText = "CAMPEÃO! 🏆";
                        document.getElementById("btn-proximo").innerText = "RECOMEÇAR";
                    }}
                }}
            }}
        }}

        function proximaFase() {{
            if(faseAtual < 3) {{
                faseAtual++;
                carregarFase();
            }} else {{
                faseAtual = 0;
                carregarFase();
            }}
        }}

        // Inicializa o jogo
        carregarFase();
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=900)
else:
    st.info("Aguardando as 4 fotos para montar o circuito...")