# **Trabalho C1.A2 — Serviço de Inferência Distribuído** 

Disciplina: Sistemas Distribuídos e Computação em Nuvem Prof. M.Sc. Howard Roatti  ·  Valor: 5,0 pontos  ·  Entrega: 17/09/2026 (Aula 7) 

_Última atualização: 01/08/2026_ 

_Você vai construir o primeiro tijolo da plataforma que acompanhará todo o semestre: um serviço que recebe um texto, executa uma inferência de IA e devolve o resultado. O desafio não está na IA (o modelo já vem pronto no kit de partida), e sim em expor esse serviço por duas tecnologias de comunicação diferentes e em não deixar o cliente esperando._ 

## **Edital** 

_Leia todo o edital antes de começar. Só será corrigido o trabalho que seguir estas orientações; caso contrário, a avaliação será desconsiderada._ 

**0 -** Formação de grupos é LIVRE (inclusive individual). Se optar por grupo, envie os nomes dos componentes ao professor até 16/09/2026 no endereço howardcruzroatti@gmail.com. 

**1 -** O tema é fixo: um serviço que recebe um texto, executa uma inferência de IA (o modelo já vem pronto no kit) e devolve o resultado. Você NÃO escolhe o domínio de negócio — o foco é a engenharia distribuída, não a IA. 

**2 -** Servir o modelo de IA do kit por DUAS interfaces de comunicação: 

- uma interface REST, construída com FastAPI; 

- uma interface gRPC, a partir de um contrato .proto. 

- as duas interfaces devem produzir o MESMO resultado para a mesma entrada. 

**3 -** Processar as inferências de forma ASSÍNCRONA: 

   - a rota de submissão coloca a tarefa em uma fila e devolve um identificador; 

   - um worker consome a fila, executa a inferência e guarda o resultado; 

   - uma segunda rota permite consultar o resultado pelo identificador. 

- **4 -** Tratar erros de forma explícita e registrar log de cada requisição recebida. 

- **5 -** Escrever um README que permita a qualquer pessoa executar o projeto do zero. 

**6 -** Extensões opcionais (não valem nota extra, mas enriquecem o trabalho e o seu portfólio): 

   - Subir mais de um worker e demonstrar a divisão de carga. 

   - Processar em lote (batch) várias entradas em uma única chamada. 

   - Cache de resultados para entradas repetidas. 

   - Medir e expor a latência média das inferências. 

- **7 -** Entregáveis: 

   - Todo o código no repositório do GitHub do grupo, organizado em diretórios (não compactado). 

   - README explicando a arquitetura e como executar o projeto do zero. 

   - No AVA, poste APENAS o link do repositório do GitHub (se o AVA exigir arquivo, envie um documento com o link). 

   - Entrega no repositório, SEM apresentação oral. 

**8 -** Distribuição da pontuação (total 5,0): 

|**Nota**|**Critério**|**Oque se avalia**|
|---|---|---|
|**1,5**|Arquitetura e decomposição em<br>serviços|Arquitetura e decomposição: separação<br>clara entre API, fila e worker.|
|**1,5**|Comunicação funcionando (REST /<br>gRPC / mensageria)|Comunicação: REST e gRPC funcionando<br>e coerentes entre si.|
|**1,0**|Resiliência e tratamento de falhas|Resiliência: tratamento de erros e log<br>das requisições.|
|**1,0**|Execução reproduzível (README,<br>container, deploy)|Execução: README claro; o projeto<br>sobe do zero seguindo o próprio<br>README.<br>_ii_|
|**5,0**|**TOTAL**|_Sofisticação do modelo de IA NÃO_<br>_pontua._|



_A qualidade ou a sofisticação do modelo de IA NÃO compõe a nota. A inteligência artificial é a carga de trabalho do sistema, não o objeto de avaliação. Todo contato com IA neste trabalho é chamada de biblioteca ou de API: não é necessário treinar modelos nem dominar matemática de aprendizado de máquina._ 

- **9 -** Kit de partida: https://github.com/howardroatti/sd-2026-2-kit-c1a2 

   - Faça um fork (cópia) do kit e estude-o ANTES de começar o seu projeto. 

   - O modelo de IA já vem pronto; concentre o esforço na engenharia distribuída. 

   - Não deixe para a última hora: o projeto cresce ao longo do bloco. 

   - Não serão aceitos projetos idênticos ou cópias parciais. 

## **Observações importantes** 

- Se for em grupo, todos os componentes devem participar do desenvolvimento; membros que não contribuírem podem ter a nota individual ajustada. 

- O trabalho NÃO possui avaliação substitutiva. 

- Atrasos serão tolerados, porém com perda de 0,5 ponto por dia de atraso. 

- Mantenha o GitHub atualizado com commits ao longo do período (e não um único commit no final). 

## **FAQ — Perguntas Frequentes** 

### **Preciso saber machine learning?** 

Não. O modelo já vem pronto e configurado no kit. Todo contato com IA é chamada de biblioteca ou de API — você não treina modelos nem precisa de matemática de ML. 

### **Preciso de internet ou GPU no laboratório?** 

Não. O kit funciona 100% offline: o modelo é treinado localmente (scikit-learn) e o cliente de LLM tem modo simulado quando não há chave de API. 

### **O trabalho é em grupo?** 

Grupos livres, a critério de vocês — inclusive individual. Se optarem por grupo, todos os componentes devem participar do desenvolvimento. 

### **Tem apresentação?** 

Não. A entrega é no repositório do GitHub, sem apresentação oral. A avaliação recai sobre o sistema funcionando, a arquitetura e as decisões de projeto. 

### **Posso usar IA para me ajudar a programar?** 

Sim, é realista e permitido. O que se avalia é o sistema funcionando e as decisões de arquitetura — que você precisa saber explicar. 

### **Posso usar outra linguagem?** 

O kit é em Python porque é o ecossistema usado nas aulas. Se quiser outra linguagem, combine com o professor antes de começar. 

### **Existe avaliação substitutiva para o trabalho?** 

Não. O trabalho não possui avaliação substitutiva. 

### **E se eu atrasar a entrega?** 

Atrasos serão tolerados, porém com perda de 0,5 ponto por dia de atraso. 

## **Roteiro sugerido de execução** 

1. Carregue o modelo UMA vez, na inicialização do serviço — nunca a cada requisição. 

2. Comece pela interface REST (Aula 5) e só depois acrescente a gRPC (Aula 4). 

3. A fila é o que você fez na Aula 8 do laboratório; reaproveite o código. 

4. Antes de entregar, apague a pasta do projeto, clone do zero e siga o seu próprio README. 

_Antes de entregar: apague a pasta do projeto, clone do zero e siga o SEU próprio README. Se funcionar, está pronto para entrega._ 

