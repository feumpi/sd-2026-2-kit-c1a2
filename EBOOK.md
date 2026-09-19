# **Sistemas Distribuídos e Computação em Nuvem** 

_Um guia de estudo cloud-native, com Inteligência Artificial como serviço_ 

###### **Prof. M.Sc. Howard Roatti** 

FAESA — Faculdades Integradas Espírito-Santenses 

**Semestre 2026/2** 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

### **Apresentação** 

###### **Sobre este livro** 

Este ebook acompanha a disciplina Sistemas Distribuídos e Computação em Nuvem. Ele foi escrito a partir das apresentações de aula, mas traz mais profundidade: onde o slide apresenta um tópico em uma linha, aqui você encontra a explicação completa, com exemplos e o porquê de cada decisão de projeto. 

A ordem dos capítulos segue exatamente a ordem das 17 aulas do semestre, organizadas em três blocos — C1 (comunicação), C2 (coordenação) e C3 (nuvem e operação). Você pode ler em sequência, acompanhando as aulas, ou usar o livro como referência para revisar um tópico específico. 

###### **Como o livro está organizado** 

Cada capítulo abre com o que você será capaz de fazer ao final dele. Em seguida vêm as seções de conteúdo, escritas em linguagem direta. Ao longo do texto você encontra estas marcações: 

- Os termos-chave aparecem em negrito na primeira vez que são explicados. São exatamente os termos que reaparecem nas caixas ao final do capítulo — quando você reencontrar um deles na revisão, já terá visto sua explicação no texto. 

- O quadro EM RESUMO condensa a ideia central de cada seção em uma frase — é o que você leva para a prova. 

- A caixa FOCO ENADE destaca o que costuma ser cobrado no Exame Nacional de Desempenho dos Estudantes, com os termos-chave que você precisa dominar. 

- O GLOSSÁRIO ao final de cada capítulo reúne, em uma linha cada, as definições dos termos novos. 

Os capítulos que fecham cada bloco (7, 12 e 17) são de revisão e trazem QUESTÕES COMENTADAS no formato do ENADE, resolvidas passo a passo. 

###### **Uma palavra sobre o ENADE** 

O ENADE 2026 será aplicado em 29 de novembro e inclui os cursos de Análise e Desenvolvimento de Sistemas, Ciência da Computação e Sistemas de Informação — ou seja, todos os cursos desta turma. Sistemas distribuídos, redes, computação em nuvem, segurança da informação e bancos de dados distribuídos são eixos recorrentes da prova. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

Por isso, as caixas FOCO ENADE não são enfeite: elas apontam, aula a aula, exatamente o que tem maior probabilidade de aparecer no exame. O Apêndice A reúne todos esses pontos em um mapa único, que serve como roteiro final de revisão. 

###### **Sobre a Inteligência Artificial neste livro** 

A IA aparece o tempo todo, mas sempre como carga de trabalho — um serviço a ser servido, escalado e protegido — e nunca como objeto de estudo em si. Você não precisará treinar modelos nem dominar a matemática de aprendizado de máquina. Todo contato com IA se resume a chamar uma biblioteca ou uma API. O que se aprende aqui é a engenharia de sistemas distribuídos que sustenta qualquer aplicação de IA moderna. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

### **Sumário** 

|Apresentação............................................................................................................................. 2|
|---|
|Sobre este livro....................................................................................................................... 2|
|Como o livro está organizado................................................................................................... 2|
|Uma palavra sobre o ENADE.................................................................................................... 2|
|Sobre a Inteligência Artificial neste livro................................................................................... 3|
|Sumário..................................................................................................................................... 4|
|Comunicação distribuída............................................................................................................. 6|
|Abertura, diagnóstico e ambiente............................................................................................ 7|
|Modelos de arquitetura e sockets (TCP/UDP)......................................................................... 10|
|Concorrência: um servidor para vários clientes....................................................................... 13|
|Do RPC ao gRPC: chamada remota moderna........................................................................... 16|
|Serviços web: REST e OpenAPI com FastAPI............................................................................ 19|
|IA como serviço distribuído (marco do curso)......................................................................... 22|
|Revisão e Avaliação C1.A1 + entrega do C1.A2........................................................................ 25|
|Coordenação e consistência...................................................................................................... 29|
|Mensageria, eventos e API Gateway...................................................................................... 30|
|Tempo e ordenação: relógios lógicos..................................................................................... 33|
|Replicação, consistência e o teorema CAP.............................................................................. 36|
|Consenso (Raft) e resiliência.................................................................................................. 39|
|Revisão e Avaliação C2.A1 + entrega do C2.A2........................................................................ 42|
|Nuvem, implantação e segurança.............................................................................................. 46|
|Computação em nuvem, containers e o primeiro deploy......................................................... 47|
|Orquestração, serverless e computação na borda................................................................... 50|
|Observabilidade: enxergar o que acontece no sistema............................................................ 53|
|Segurança, LGPD e revisão geral para o ENADE....................................................................... 55|
|Avaliação C3.A1, entrega do C3.A2 e tendências..................................................................... 58|



Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

|Apêndice A — Mapa de revisão para o ENADE............................................................................ 62|
|---|
|Apêndice B — Bibliografia e materiais de apoio.......................................................................... 65|
|Básica................................................................................................................................... 65|
|Complementar...................................................................................................................... 65|
|Materiais abertos.................................................................................................................. 65|



Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

##### **PARTE C1** 

## **Comunicação distribuída** 

Aulas 1 a 7 

_Como dois programas conversam de forma confiável através da rede. Dos sockets à IA servida por API, passando por concorrência, gRPC e REST._ 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 1  ·  C1  ·  06/08/2026** 

#### **Abertura, diagnóstico e ambiente** 

**Neste capítulo você vai aprender a:** 

- Explicar o que é um sistema distribuído e por que quase todo software hoje é um. 

- Reconhecer o desafio que só existe quando há rede no meio: a falha parcial. 

- Deixar seu ambiente pronto: máquina virtual, Python, Git e GitHub. 

###### **O que muda quando existe uma rede no meio** 

Um programa comum roda inteiro dentro de uma máquina: se algo dá errado, o processo simplesmente para, e você vê o erro. Um **sistema distribuído** é diferente por natureza — ele é formado por vários computadores independentes que cooperam pela rede e se apresentam ao usuário como se fossem um sistema único. Quando você abre o aplicativo do banco, dezenas de máquinas em lugares diferentes trabalham para responder ao seu toque na tela, mas você enxerga apenas o saldo. 

Essa cooperação pela rede traz três ganhos que um programa isolado nunca teria. O primeiro é a **escalabilidade** : a capacidade de atender a uma demanda crescente acrescentando mais máquinas, em vez de depender de um único computador cada vez maior. O segundo é a disponibilidade, já que o serviço pode continuar de pé mesmo que uma máquina caia. O terceiro é a proximidade do usuário, colocando servidores em várias regiões. Em troca, aceita-se um custo que não existe no programa local: a rede é lenta, imprevisível e, principalmente, falha — e não falha de forma limpa. 

###### **Latência e transparência** 

Duas ideias acompanham todo o curso. A primeira é a **latência** : o tempo que uma mensagem leva para ir de um ponto a outro da rede. Diferente do acesso à memória local, medido em nanossegundos, uma chamada de rede custa milissegundos — e esse tempo é variável, porque a mensagem disputa a rede com todo o resto. Boa parte das decisões de projeto que veremos existe para esconder ou reduzir a latência. 

A segunda ideia é a **transparência** : o esforço de esconder do usuário a complexidade da distribuição. Há vários tipos — transparência de acesso (usar um recurso remoto como se fosse local), de localização (não precisar saber em qual máquina o dado está) e de replicação (não perceber que existem várias cópias). Quanto maior a transparência, mais simples o sistema parece por fora, e mais trabalho ele exige por dentro. 

###### **Falha parcial: o problema central da disciplina** 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

Num sistema centralizado, a falha é total: ou tudo funciona, ou tudo para, e fica evidente qual foi o caso. Num sistema distribuído surge a **falha parcial** — uma parte do sistema para enquanto o resto continua funcionando. Pior que isso é a ambiguidade que ela cria. Quando um serviço A envia um pedido a um serviço B e não recebe resposta, A não tem como saber o que aconteceu: B pode ter caído, pode estar apenas lento, ou a resposta pode ter se perdido no caminho de volta. Do ponto de vista de A, essas três situações são indistinguíveis. 

Guarde esta ideia, porque praticamente todo o resto da disciplina é uma resposta a ela. Os relógios lógicos, o teorema CAP, o consenso, os padrões de resiliência — tudo existe porque a falha parcial é real e inevitável. Aprender sistemas distribuídos é, em boa medida, aprender a projetar contando com ela. 

###### **O que você vai construir e onde guardá-lo** 

O fio condutor prático do curso é uma plataforma de IA como serviço. Ela nasce como um simples par cliente-servidor trocando mensagens e, aula após aula, ganha interfaces modernas, uma fila, microsserviços, containers e, por fim, é publicada na nuvem. A IA entra apenas como a tarefa que esse sistema executa: você chama um modelo pronto, nunca o treina. Desde o primeiro dia, todo esse código é versionado num **repositório** — a pasta controlada pelo Git onde você guarda o histórico do projeto e o envia para o GitHub. Trabalhar em repositório não é burocracia: é como equipes reais colaboram e como você provará, ao final, tudo o que construiu. 

###### **NO SEU TRABALHO — C1.A2: Serviço de Inferência Distribuído** 

<mark>O trabalho da primeira verificação — o</mark> **<mark>C1.A2 — Serviço de Inferência Distribuído</mark>** <mark>— começa hoje pela base: preparar o ambiente e criar o repositório onde ele vai crescer. O kit de partida já traz o modelo de IA pronto e o esqueleto do projeto.</mark> 

- Clonar o repositório `sd-2026-2-kit-c1a2` e criar o seu repositório de entrega. 

- Rodar o exemplo mínimo cliente-servidor que acompanha o kit. 

- <mark>Ler o</mark> `TAREFAS.md` <mark>, que lista o núcleo obrigatório item a item.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c1a2_ 

###### **EM RESUMO** 

Sistema distribuído = várias máquinas cooperando que parecem uma só. 

A dificuldade não é a rede ser lenta: é você não saber o que aconteceu do outro lado. <mark>Você aprende sistemas distribuídos construindo um serviço de IA de verdade.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Questões introdutórias pedem a definição de</mark> **<mark>sistema distribuído</mark>** <mark>e o contraste com sistemas centralizados, os tipos de</mark> **<mark>transparência</mark>** <mark>(acesso, localização, replicação) e as justificativas para</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

<mark>distribuir —</mark> **<mark>escalabilidade</mark>** <mark>, disponibilidade e desempenho. A noção de</mark> **<mark>falha parcial</mark>** <mark>aparece</mark> disfarçada em estudos de caso, e a **latência** costuma justificar decisões de arquitetura. 

**<mark>Costuma cair:</mark>** <mark>Conceito e caracterização de sistemas distribuídos.; Vantagens e desafios: escalabilidade, disponibilidade e falha parcial.; Diferença entre sistema centralizado e sistema</mark> distribuído.; Tipos de transparência (acesso, localização, replicação). 

**<mark>Termos-chave:</mark>** <mark>Sistema distribuído · Falha parcial · Transparência · Escalabilidade · Latência</mark> 

###### **QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Um serviço A envia uma requisição ao serviço B e não recebe resposta no tempo esperado. Sobre essa situação em um sistema distribuído, assinale a alternativa correta.</mark> 

- **(A)** A pode concluir com certeza que B falhou. 

- **(B)** A pode concluir que a requisição certamente não foi processada. 

**<mark>(C)</mark>** <mark>A não distingue, apenas pela ausência de resposta, entre B ter caído, estar lento ou a resposta</mark> ter se perdido. 

- **(D)** A deve encerrar todo o sistema, pois trata-se de falha total. 

- **<mark>(E)</mark>** <mark>A situação não ocorre quando se utiliza TCP.</mark> 

**<mark>Resolução.</mark>** <mark>É a definição de falha parcial: a ausência de resposta é ambígua. O TCP não elimina o problema, pois B pode cair após receber o pedido. As demais alternativas afirmam certezas que A</mark> não possui. 

**Resposta. Alternativa C.** 

###### **GLOSSÁRIO DO CAPÍTULO** 

**<mark>Sistema distribuído</mark>** <mark>Computadores independentes que cooperam e se apresentam como um</mark> sistema único. 

**Falha parcial** Uma parte do sistema falha enquanto o restante continua funcionando. **Latência** Tempo que uma mensagem leva para ir de um ponto a outro da rede. 

**Transparência** Esconder do usuário a complexidade da distribuição. 

**<mark>Repositório</mark>** <mark>Pasta versionada pelo Git onde você guarda e envia seu código.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 2  ·  C1  ·  13/08/2026** 

#### **Modelos de arquitetura e sockets (TCP/UDP)** 

**Neste capítulo você vai aprender a:** 

- Diferenciar os modelos cliente-servidor e ponto a ponto (P2P). 

- Explicar, com suas palavras, a diferença prática entre TCP e UDP. 

- Escrever um cliente e um servidor que trocam mensagens por socket. 

###### **Cliente-servidor e ponto a ponto** 

Há duas formas básicas de organizar quem fala com quem. No modelo **cliente-servidor** , os papéis são fixos: um lado pede (o cliente) e o outro responde (o servidor). É o modelo dominante na web e em quase todo serviço que você usa. No modelo ponto a ponto — ou **P2P** , de peer-to-peer — todos os participantes têm o mesmo papel e trocam informação diretamente entre si, sem um servidor central; o BitTorrent é o exemplo clássico, em que cada participante baixa e envia ao mesmo tempo. 

A escolha tem consequências. O servidor central é simples de gerenciar e proteger, mas concentra carga e é um ponto único de falha. O P2P distribui a carga e não tem um centro que possa cair, mas é bem mais difícil de coordenar, versionar e proteger. A maioria dos sistemas que você vai construir é cliente-servidor; o P2P aparece quando escala e resiliência importam mais que controle. 

###### **Socket: a ponta do cano** 

Toda comunicação em rede, por baixo, passa por sockets. Um **socket** é a ponta de uma conexão, identificada pela combinação de endereço IP e **porta** — o IP diz em qual máquina, e a porta diz qual programa dentro dela deve receber a mensagem. É por isso que um mesmo servidor pode rodar um site na porta 443 e um banco de dados na 5432 sem confusão: cada serviço escuta a sua. O servidor abre a porta e fica aguardando (as operações bind, listen e accept); o cliente se conecta àquela porta (connect); e então os dois trocam bytes. Tudo o que vem depois no curso — gRPC, REST, filas — roda sobre essa base. 

###### **TCP ou UDP: garantia contra velocidade** 

Sobre o socket você escolhe o protocolo de transporte, e a escolha é um trade-off honesto. O **TCP** estabelece uma conexão antes de enviar dados, garante que eles cheguem na ordem certa e retransmite o que se perde; em troca, tudo isso custa tempo e alguns pacotes de controle. O **UDP** não estabelece conexão e não garante nada: é rápido e leve, mas pacotes podem se perder ou chegar fora de ordem, e cabe à sua aplicação lidar com isso. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

A regra prática é clara. Use TCP quando não pode perder dado: um arquivo, uma mensagem de chat, uma transação bancária — nesses casos, receber tudo, na ordem, importa mais que a pressa. Use UDP quando o atraso é pior que a perda: voz, vídeo ao vivo, jogos online, telemetria de sensores — é melhor descartar um quadro atrasado do que travar a imagem esperando por ele. Muitos protocolos modernos, como o do vídeo em tempo real, escolhem UDP justamente por isso. 

###### **NO SEU TRABALHO — C1.A2: Serviço de Inferência Distribuído** 

<mark>Sockets são o alicerce invisível do trabalho: as interfaces gRPC e REST que você vai expor rodam sobre eles. Você não os programa diretamente, mas entender esta camada explica por que uma chamada ao serviço pode ficar</mark> ' <mark>pendurada</mark> ' <mark>.</mark> 

- <mark>Compreender a base sobre a qual as interfaces do C1.A2 serão construídas — fundamento para</mark> 

- <mark>o tempo-limite que você adicionará na fase de resiliência.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c1a2_ 

###### **EM RESUMO** 

Cliente-servidor tem papéis fixos; em P2P todos fazem os dois papéis. 

Socket = IP + porta. O servidor espera na porta; o cliente conecta nela. 

<mark>TCP garante entrega e ordem, mas custa tempo. UDP é rápido, porém pode perder e desordenar.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Um dos tópicos mais cobrados. Espere cenários (streaming, transferência de arquivo, telemetria) que pedem a escolha justificada entre</mark> **<mark>TCP</mark>** <mark>e</mark> **<mark>UDP</mark>** <mark>. Também são comuns questões sobre o conceito</mark> de **socket** e **porta** , sobre **cliente-servidor** versus **P2P** , e sobre as camadas do modelo TCP/IP. **<mark>Costuma cair:</mark>** <mark>Modelo cliente-servidor comparado ao modelo P2P.; Características de TCP e UDP e critério para escolher entre eles.; Conceito de socket, porta e endereçamento.; Camadas do modelo</mark> TCP/IP e encapsulamento. 

**<mark>Termos-chave:</mark>** <mark>Cliente-servidor · P2P · Socket · Porta · TCP · UDP</mark> 

###### **QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Uma aplicação de voz sobre IP prioriza baixa latência e tolera a perda ocasional de pequenos trechos de áudio. Qual protocolo de transporte é o mais adequado e por quê?</mark> 

- **(A)** TCP, porque garante a entrega ordenada de todos os pacotes. 

- **(B)** TCP, porque realiza controle de fluxo e congestionamento. 

- **(C)** UDP, porque não retransmite pacotes perdidos, evitando o atraso acumulado. 

- **(D)** UDP, porque confirma o recebimento de cada pacote enviado. 

- **<mark>(E)</mark>** <mark>UDP, porque estabelece conexão prévia e reduz a latência.</mark> 

**<mark>Resolução.</mark>** <mark>Em mídia de tempo real, o atraso é pior que a perda; o UDP não retransmite e mantém o fluxo fluido. As alternativas D e E descrevem o UDP incorretamente — ele não confirma</mark> recebimento nem estabelece conexão. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**Resposta. Alternativa C. GLOSSÁRIO DO CAPÍTULO Socket** Ponta de uma conexão de rede, identificada por IP e porta. **Porta** Número que identifica qual programa da máquina recebe a mensagem. **TCP** Protocolo com conexão que garante entrega e ordem das mensagens. **UDP** Protocolo sem conexão, rápido, que não garante entrega nem ordem. **<mark>P2P</mark>** <mark>Arquitetura em que todos os participantes têm o mesmo papel.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 3  ·  C1  ·  20/08/2026** 

#### **Concorrência: um servidor para vários clientes** 

**Neste capítulo você vai aprender a:** 

- Explicar por que um servidor simples atende apenas um cliente por vez. 

- Usar threads para atender vários clientes ao mesmo tempo. 

- Identificar e corrigir uma condição de corrida em estado compartilhado. 

###### **Por que um servidor simples atende um cliente por vez** 

As chamadas de rede como accept() e recv() são **bloqueantes** : elas param a execução do programa até que algo aconteça — uma conexão chegar, um dado ser recebido. Num servidor escrito de forma sequencial, isso significa que, enquanto ele atende um cliente, todos os outros ficam esperando na fila. Basta um cliente lento — ou mal-intencionado — para travar o atendimento de todos. Para um serviço real, com muitos usuários simultâneos, isso é inaceitável. 

###### **Uma thread por cliente** 

A solução clássica é a concorrência: transformar cada atendimento em uma **thread** , uma linha de execução independente dentro do mesmo programa. Quando o servidor aceita uma conexão, ele entrega aquele cliente a uma thread própria e volta imediatamente para o accept(), pronto para o próximo. Assim, muitos clientes são atendidos ao mesmo tempo, e um cliente lento atrapalha apenas a sua própria thread. Vale distinguir concorrência de paralelismo: concorrência é lidar com várias tarefas em andamento (revezando o processador), enquanto paralelismo é executá-las literalmente ao mesmo tempo, em núcleos diferentes. 

###### **O preço da concorrência: condição de corrida** 

A concorrência resolve um problema e cria outro. Se duas threads alteram a mesma variável ao mesmo tempo, o resultado fica imprevisível — é a **condição de corrida** . O exemplo clássico é um contador: duas threads leem o valor 41, ambas somam 1 e ambas gravam 42, quando o correto seria 43; uma das contagens se perdeu. O sintoma é traiçoeiro, porque o erro aparece só às vezes, dependendo do momento exato em que as threads se cruzam, o que torna a depuração difícil. 

A proteção fundamental é a **exclusão mútua** : garantir que apenas uma thread por vez execute o trecho de código que mexe no dado compartilhado — a **seção crítica** . Na prática, isso é feito com um **lock** (uma trava): a thread adquire o lock ao entrar na seção 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

crítica e o libera ao sair, de modo que as demais esperam a vez. Esta ideia — acesso concorrente a estado compartilhado — reaparece o semestre inteiro, agora entre máquinas diferentes em vez de threads: as réplicas de um banco de dados enfrentam uma versão distribuída exatamente do mesmo problema. 

###### **NO SEU TRABALHO — C1.A2: Serviço de Inferência Distribuído** 

<mark>O seu serviço processa inferências em segundo plano com um</mark> **<mark>worker</mark>** <mark>, e a concorrência desta aula é o que o sustenta. A fila em si já vem pronta no kit; a teoria por trás dela virá na Aula 8.</mark> 

- TAREFA 3 — fazer o worker gravar o resultado processado para consulta posterior. 

- <mark>TAREFA 5 — tratamento de erro no worker (retentativa).</mark> 

**Repositório do kit:** _sd-2026-2-kit-c1a2_ 

###### **EM RESUMO** 

Um servidor sequencial atende um cliente por vez; os demais esperam. 

Uma thread por cliente libera o laço principal para aceitar o próximo. 

<mark>Concorrência sem controle corrompe dado compartilhado. Proteja a seção crítica com lock.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Concorrência é tema recorrente. Domine a diferença entre concorrência e paralelismo e os conceitos de</mark> **<mark>condição de corrida</mark>** <mark>,</mark> **<mark>exclusão mútua</mark>** <mark>,</mark> **<mark>seção crítica</mark>** <mark>,</mark> **<mark>lock</mark>** <mark>e chamada</mark> **<mark>bloqueante</mark>** <mark>. Questões costumam mostrar um contador incorreto ou um cenário de acesso simultâneo e pedir o</mark> diagnóstico e a correção. 

**<mark>Costuma cair:</mark>** <mark>Concorrência e paralelismo: diferença entre os dois.; Condição de corrida, exclusão mútua e seção crítica.; Threads e processos: quando usar cada um.; Escalabilidade de servidores e</mark> gargalos. 

**<mark>Termos-chave:</mark>** <mark>Thread · Condição de corrida · Exclusão mútua · Seção crítica · Lock · Bloqueante</mark> 

###### **QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Duas threads incrementam a mesma variável sem sincronização e o total final fica menor que o esperado. Qual é o problema e a correção adequada?</mark> 

- **(A)** Deadlock; aumentar o número de threads. 

- **(B)** Condição de corrida; proteger a seção crítica com exclusão mútua. 

**(C)** Inanição (starvation); elevar a prioridade das threads. 

- **(D)** Falha de rede; substituir o protocolo de transporte. 

- **<mark>(E)</mark>** <mark>Cold start; pré-aquecer o serviço.</mark> 

**<mark>Resolução.</mark>** <mark>Acesso concorrente não sincronizado a dado compartilhado é uma condição de</mark> corrida; corrige-se garantindo exclusão mútua na seção crítica, com um lock. 

**Resposta. Alternativa B.** 

**GLOSSÁRIO DO CAPÍTULO** 

**Thread** Linha de execução independente dentro do mesmo programa. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**<mark>Condição de corrida</mark>** <mark>Erro que ocorre quando duas threads alteram o mesmo dado ao mesmo</mark> tempo. 

**Seção crítica** Trecho de código que só pode ser executado por uma thread por vez. **Lock** Mecanismo que garante exclusão mútua na seção crítica. 

**<mark>Bloqueante</mark>** <mark>Chamada que para a execução até que a operação termine.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 4  ·  C1  ·  27/08/2026** 

#### **Do RPC ao gRPC: chamada remota moderna** 

**Neste capítulo você vai aprender a:** 

- Explicar a ideia de chamada remota de procedimento (RPC). 

- Escrever um contrato .proto com Protocol Buffers. 

- Implementar um servidor e um cliente gRPC em Python. 

###### **A ideia do RPC** 

A chamada remota de procedimento — **RPC** , de Remote Procedure Call — nasceu de um desejo simples: fazer uma função que está em outra máquina parecer uma função local. Em vez de escrever bytes no socket e interpretá-los na mão, você chama algo como servico.somar(2, 3) e o **middleware** (a camada de software que fica entre a sua aplicação e a rede) cuida de empacotar os argumentos, enviá-los, receber o resultado e devolvê-lo. A linha do tempo dessa ideia passa pelo RPC clássico, pelo CORBA, pelo **RMI** — a Invocação de Métodos Remotos do Java, que aplica a mesma ideia a objetos — e chega, hoje, ao **gRPC** . A ementa fala de RPC e RMI; tratamos ambos como a origem do gRPC. 

###### **Serialização e o contrato: Protocol Buffers** 

Para trafegar pela rede, uma estrutura de dados precisa virar uma sequência de bytes e depois ser remontada do outro lado — esse processo de ida e volta é a **serialização** . No gRPC, o formato de serialização e o contrato do serviço são descritos num arquivo com a extensão .proto, usando **Protocol Buffers** . Nele você declara quais operações o serviço oferece e quais mensagens trafegam, com seus campos e tipos. Uma ferramenta lê esse arquivo e gera automaticamente o código de cliente e de servidor — os **stubs** , que são justamente os trechos que escondem a rede e fazem a chamada remota parecer local. O ponto importante é a inversão: o contrato existe antes do código, e os dois lados são obrigados a respeitá-lo. 

###### **Por que o gRPC é usado hoje** 

Três características explicam a adoção. Primeiro, a serialização binária do Protocol Buffers é compacta — trafega muito menos bytes que texto como JSON ou XML. Segundo, o gRPC roda sobre HTTP/2, o que permite várias chamadas na mesma conexão, sem reabri-la a cada pedido. Terceiro, o contrato é tipado, então erros de tipo aparecem cedo, na geração dos stubs, e não em produção. Por isso o gRPC é a escolha natural para a comunicação interna entre serviços — inclusive entre os microsserviços de IA que você vai construir. Para 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

o público externo, porém, o REST ainda costuma vencer pela simplicidade de consumo, como veremos a seguir. 

**NO SEU TRABALHO — C1.A2: Serviço de Inferência Distribuído** 

<mark>Uma das duas interfaces exigidas pelo C1.A2 é gRPC. Com o contrato</mark> `.proto` <mark>e os stubs desta aula, você implementa o método do serviço.</mark> 

- <mark>TAREFA 4 — implementar o método gRPC</mark> `PreverLote` <mark>e regerar os stubs.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c1a2_ 

**EM RESUMO** 

RPC faz uma chamada remota parecer uma chamada de função local. 

O .proto é o contrato: define mensagens e operações antes do código existir. 

<mark>gRPC = contrato tipado + formato binário + HTTP/2. Padrão para serviço falar com serviço.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Espere questões sobre o conceito de</mark> **<mark>RPC</mark>** <mark>e de invocação remota de métodos (</mark> **<mark>RMI</mark>** <mark>), sobre transparência de acesso e sobre o papel do</mark> **<mark>middleware</mark>** <mark>e dos</mark> **<mark>stubs</mark>** <mark>. A</mark> **<mark>serialização</mark>** <mark>— converter estruturas de dados em bytes para trafegar na rede — costuma aparecer junto, assim como a</mark> comparação entre **gRPC** e outras formas de integração. 

**<mark>Costuma cair:</mark>** <mark>Conceito de RPC e transparência de acesso.; RMI e invocação de métodos</mark> remotos.; Serialização e representação de dados na rede.; Middleware de comunicação e stubs. **<mark>Termos-chave:</mark>** <mark>RPC · RMI · gRPC · Protocol Buffers · Stub · Serialização · Middleware</mark> 

**QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>No gRPC, qual é a função do arquivo com extensão .proto?</mark> 

- **(A)** Conter a implementação completa do servidor. 

- **(B)** Definir o contrato (mensagens e operações), a partir do qual se geram os stubs. 

- **(C)** Ser gerado automaticamente após a implementação do servidor. 

**(D)** Eliminar a necessidade de comunicação em rede. 

**<mark>(E)</mark>** <mark>Armazenar as credenciais de autenticação do serviço.</mark> 

**<mark>Resolução.</mark>** <mark>O .proto é o contrato e vem antes do código; a ferramenta gera, a partir dele, os stubs</mark> de cliente e de servidor. 

**Resposta. Alternativa B.** 

###### **GLOSSÁRIO DO CAPÍTULO** 

**RPC** Chamada de procedimento remoto: invocar uma função que está em outra máquina. **gRPC** Framework atual de RPC, binário, sobre HTTP/2, com contrato em .proto. 

**Protocol Buffers** Formato binário de serialização usado para definir o contrato. 

**Stub** Código gerado que representa o serviço remoto no cliente e no servidor. 

**<mark>Middleware</mark>** <mark>Camada de software que cuida da comunicação entre partes distribuídas.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 5  ·  C1  ·  10/09/2026** 

#### **Serviços web: REST e OpenAPI com FastAPI** 

**Neste capítulo você vai aprender a:** 

- Explicar os princípios REST e a diferença para o SOAP. 

- Construir uma API REST com FastAPI usando os verbos e códigos corretos. 

- Ler e usar a documentação automática gerada pelo OpenAPI. 

###### **Do SOAP ao REST** 

Serviços web permitem que sistemas diferentes conversem pela internet. A geração anterior, o **SOAP** , usava mensagens em XML e um contrato rígido descrito em WSDL; era poderoso, porém verboso e pesado, e ainda sobrevive em sistemas legados e bancários. O **REST** (Representational State Transfer), dominante hoje, é bem mais simples: em vez de uma camada extra sobre o protocolo, ele usa o próprio HTTP como ele já é. A ementa cita os dois, mas um serviço novo nasce REST — ou gRPC — e quase nunca SOAP. Saber os dois é útil para entender a evolução da chamada Arquitetura Orientada a Serviços (SOA) rumo aos microsserviços. 

###### **Recursos, verbos e códigos de status** 

O REST organiza tudo em torno de **recursos** , que são substantivos e viram URLs: /tarefas para a coleção, /tarefas/7 para um item específico. A ação desejada é dada pelo **verbo HTTP** : GET lê, POST cria, PUT atualiza e DELETE remove. E o resultado é comunicado pelo **código de status** : 200 para sucesso, 201 para recurso criado, 400 para erro do cliente, 404 para recurso inexistente, 500 para erro do servidor. Essa separação clara — a URL diz o quê, o verbo diz a ação, o status diz o resultado — é o que torna uma API REST previsível para quem a consome. 

Uma propriedade importante é a **idempotência** : uma operação é idempotente quando, repetida, leva ao mesmo estado final. GET, PUT e DELETE são idempotentes; POST não é, porque cada chamada cria um novo recurso. Guarde essa distinção: ela volta a importar quando falarmos de retentativa, porque só é seguro repetir automaticamente uma operação idempotente. 

###### **OpenAPI: a documentação que não envelhece** 

Um bom serviço REST precisa de um contrato para quem vai consumi-lo. Com o FastAPI, esse contrato — no padrão **OpenAPI** — é gerado automaticamente a partir dos tipos declarados no seu código, e fica disponível numa página interativa. Como nasce do próprio 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

código, a documentação não fica desatualizada, um problema crônico da era SOAP, em que o contrato e a implementação viviam divergindo. 

###### **NO SEU TRABALHO — C1.A2: Serviço de Inferência Distribuído** 

<mark>A outra interface é REST. As rotas de submissão e de consulta do resultado são o coração da API do trabalho.</mark> 

- TAREFA 1 — `POST /predict` que enfileira a tarefa e devolve um identificador. 

- TAREFA 2 — `GET /resultado/{id}` para buscar o resultado quando pronto. 

- <mark>TAREFA 6 — registrar log de cada requisição.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c1a2_ 

###### **EM RESUMO** 

REST usa o HTTP como ele já é: recursos em URLs e verbos para operar neles. A URL diz O QUE; o verbo diz A AÇÃO; o código de status diz O RESULTADO. 

<mark>Com FastAPI, o contrato da API nasce do código — e fica sempre atualizado.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Web services aparecem com frequência: diferença entre</mark> **<mark>SOAP</mark>** <mark>e</mark> **<mark>REST</mark>** <mark>, os</mark> **<mark>verbos HTTP</mark>** <mark>e seus</mark> **<mark>códigos de status</mark>** <mark>, o conceito de</mark> **<mark>idempotência</mark>** <mark>e a documentação por</mark> **<mark>OpenAPI</mark>** <mark>. Saiba relacionar a Arquitetura Orientada a Serviços (SOA) com REST e com a interoperabilidade entre</mark> sistemas. 

**<mark>Costuma cair:</mark>** <mark>Web services: SOAP e REST, diferenças e aplicabilidade.; Verbos HTTP, códigos de status e idempotência.; Arquitetura orientada a serviços (SOA) e interoperabilidade.; Contratos de</mark> API e documentação (WSDL, OpenAPI). 

**<mark>Termos-chave:</mark>** <mark>REST · SOAP · Recurso · Verbo HTTP · Código de status · OpenAPI · Idempotência</mark> 

###### **QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Em uma API REST, para criar um novo recurso e sinalizar sucesso, o verbo e o código de status esperados são, respectivamente:</mark> 

- **(A)** GET e 200 (OK). 

- **(B)** POST e 201 (Created). 

- **(C)** PUT e 204 (No Content). 

- **(D)** POST e 404 (Not Found). 

- **<mark>(E)</mark>** <mark>DELETE e 200 (OK).</mark> 

**<mark>Resolução.</mark>** <mark>POST cria o recurso e 201 (Created) indica criação bem-sucedida. O 404 sinaliza</mark> recurso inexistente e não faz sentido como resposta de criação. 

**Resposta. Alternativa B.** 

###### **GLOSSÁRIO DO CAPÍTULO** 

**REST** Estilo de arquitetura que usa recursos em URLs e verbos HTTP. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**SOAP** Protocolo de web service baseado em XML, com contrato em WSDL. **Recurso** Entidade exposta pela API e identificada por uma URL. **Código de status** Número devolvido pelo HTTP que informa o resultado da operação. **Idempotência** Propriedade de uma operação que, repetida, não altera o resultado final. **<mark>OpenAPI</mark>** <mark>Padrão de descrição de APIs REST, gerado automaticamente pelo FastAPI.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 6  ·  C1  ·  Estudo Dirigido (EAD)** 

#### **IA como serviço distribuído (marco do curso)** 

**Neste capítulo você vai aprender a:** 

- Dominar o vocabulário mínimo de IA necessário para operar um modelo. 

- Servir um modelo de IA atrás de uma API REST. 

- Reconhecer os problemas distribuídos que a IA cria: latência e cold start. 

###### **O vocabulário mínimo de IA** 

Para servir um modelo você não precisa de matemática, mas precisa de cinco palavras. Um **modelo** é um arquivo já treinado que transforma uma entrada em uma saída. A **inferência** é o ato de usar esse modelo para obter uma resposta — na prática, é chamar uma função. Um **embedding** é a representação de um texto como uma lista de números que captura o seu significado, o que permite comparar textos por semelhança medindo a distância entre seus vetores. Um **token** é um pedaço de texto que o modelo processa por vez (uma palavra ou parte dela). E um **LLM** (Large Language Model, ou modelo de linguagem grande) é um modelo treinado em enormes volumes de texto, que consumiremos por API. Com esse vocabulário você opera qualquer serviço de IA sem abrir a 'caixa-preta'. 

###### **Servir um modelo como serviço** 

A regra de ouro é carregar o modelo uma única vez, quando o serviço sobe, e mantê-lo em memória. Carregá-lo a cada requisição seria um erro grave de projeto, porque essa é uma operação cara — envolve ler um arquivo grande do disco e prepará-lo. Feito o carregamento na inicialização, a rota /predict apenas recebe a entrada e chama a inferência. Repare que a API é a mesma que você aprendeu na aula anterior: o que muda é a carga de trabalho que ela executa por baixo. 

###### **Os problemas que a IA traz para o sistema** 

A inferência é lenta se comparada a uma consulta comum: pense em centenas de milissegundos ou segundos, não em microssegundos. Além disso, existe o **cold start** — a primeira chamada depois de o serviço subir é sempre a mais lenta, porque o ambiente ainda está sendo preparado (o modelo sendo carregado, a memória sendo alocada). Como a operação é lenta, deixar o cliente parado esperando pela resposta é um mau desenho; a solução, que veremos na próxima aula, é processar de forma assíncrona com uma fila. É justamente por ser uma carga pesada, lenta e realista que a IA é um caso de estudo tão bom 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

para sistemas distribuídos — ela expõe, na prática, todos os problemas que a teoria descreve. 

###### **NO SEU TRABALHO — C1.A2: Serviço de Inferência Distribuído** 

<mark>Aqui o C1.A2 ganha vida: o modelo (já pronto no kit) passa a ser servido de verdade, e as duas interfaces devem convergir para o mesmo resultado. É o marco de lançamento do trabalho.</mark> 

- Carregar o modelo uma única vez, na subida do serviço. 

- TAREFA 7 — escrever o README explicando arquitetura e execução. 

- <mark>Conferir que REST e gRPC devolvem o mesmo resultado para a mesma entrada.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c1a2_ 

###### **EM RESUMO** 

Modelo é um arquivo; inferência é chamar uma função. Todo o resto é engenharia. Carregue o modelo na subida do serviço; a rota apenas chama a inferência. 

<mark>IA é uma carga lenta e pesada — e é exatamente por isso que ela é um ótimo caso de estudo.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Aqui o ENADE cobra menos a IA em si e mais a arquitetura: separação de responsabilidades, desempenho e tempo de resposta de serviços, e o encaixe de</mark> ' <mark>tecnologias emergentes</mark> ' <mark>(IA como serviço) no rol de aplicações de sistemas distribuídos. Domine os termos</mark> **<mark>modelo</mark>** <mark>,</mark> **<mark>inferência</mark>** <mark>,</mark> **embedding** , **token** , **LLM** e **cold start** no sentido operacional. 

**<mark>Costuma cair:</mark>** <mark>Aplicações e casos de uso de sistemas distribuídos.; Arquitetura de serviços e separação de responsabilidades.; Desempenho, latência e tempo de resposta em serviços.;</mark> Tecnologias emergentes: inteligência artificial como serviço. 

**<mark>Termos-chave:</mark>** <mark>Inferência · Modelo · Embedding · Token · LLM · Cold start</mark> 

###### **QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Um serviço de inferência está lento; verifica-se que o modelo é carregado do disco a cada requisição. A correção mais adequada é:</mark> 

- **(A)** Substituir REST por SOAP na interface. 

- **(B)** Carregar o modelo uma única vez, na inicialização, mantendo-o em memória. 

- **(C)** Reduzir o número de rotas expostas. 

- **(D)** Trocar o protocolo de transporte de TCP para UDP. 

- **<mark>(E)</mark>** <mark>Remover a validação dos dados de entrada.</mark> 

**<mark>Resolução.</mark>** <mark>Carregar o modelo é uma operação cara e deve ocorrer uma única vez, no startup. As</mark> demais alternativas não atacam a causa do problema. 

**Resposta. Alternativa B.** 

###### **GLOSSÁRIO DO CAPÍTULO** 

**Modelo** Arquivo já treinado que transforma uma entrada em uma saída. 

**Inferência** Ato de usar o modelo para obter uma resposta. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**Embedding** Representação de um texto como lista de números que captura significado. **Token** Pedaço de texto processado pelo modelo. **LLM** Modelo de linguagem grande, normalmente consumido por API. **<mark>Cold start</mark>** <mark>Lentidão da primeira execução, antes de o serviço estar aquecido.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 7  ·  C1  ·  17/09/2026** 

#### **Revisão e Avaliação C1.A1 + entrega do C1.A2** 

**Neste capítulo você vai aprender a:** 

- Revisar de forma consolidada todos os conceitos da Verificação C1. 

- Realizar a avaliação escrita C1.A1, no estilo ENADE (5,0 pontos). 

- Entregar o trabalho prático C1.A2 (5,0 pontos). 

###### **O caminho percorrido no bloco de comunicação** 

Este capítulo fecha a primeira verificação, dedicada à pergunta: como dois programas conversam de forma confiável através da rede? Percorremos do byte cru no **socket** até um serviço de IA publicado. Vimos os modelos cliente-servidor e P2P; a diferença entre **TCP** e **UDP** ; a concorrência com **threads** e o risco de condição de corrida; a evolução do RPC até o **gRPC** , com seu contrato em Protocol Buffers; o estilo **REST** , com seus verbos e códigos de status; e, por fim, a IA servida por trás de uma API. Antes da avaliação, releia os quadros EM RESUMO de cada capítulo e confira se você sabe responder, com segurança, por que TCP difere de UDP, o que é falha parcial, o que uma thread resolve e qual problema cria, para que serve o arquivo .proto, o que determina o verbo e o código de status de uma rota REST e por que a inferência de IA muda o desenho do serviço. 

**NO SEU TRABALHO — C1.A2: Serviço de Inferência Distribuído** 

<mark>Dia de entrega do C1.A2. Antes de submeter, rode o projeto do zero e confira contra a rubrica.</mark> 

- Clonar do zero e seguir o próprio README — funciona? 

- Conferir a rubrica: arquitetura, comunicação, resiliência e execução reproduzível. 

- <mark>Entregar no repositório (sem apresentação oral).</mark> 

**Repositório do kit:** _sd-2026-2-kit-c1a2_ 

###### **Questões comentadas (estilo ENADE)** 

_Questões novas, elaboradas para esta disciplina e inspiradas nos temas e formatos das provas reais do ENADE de Computação (edições 2021 e 2024)._ 

###### **QUESTÃO COMENTADA 1** 

**<mark>Enunciado.</mark>** <mark>Uma equipe desenvolve um serviço de transmissão de áudio ao vivo. Nos testes, a retransmissão de pacotes perdidos provocava travamentos e atraso acumulado, prejudicando mais a experiência do que a perda de trechos muito curtos. O protocolo de transporte mais adequado é:</mark> 

- **(A)** TCP, por garantir entrega ordenada. 

- **(B)** TCP, por realizar controle de fluxo. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

- **(C)** UDP, por não retransmitir pacotes perdidos, evitando o atraso acumulado. 

**(D)** UDP, por confirmar cada pacote. 

**<mark>(E)</mark>** <mark>UDP, por estabelecer conexão prévia.</mark> 

**<mark>Resolução.</mark>** <mark>Em tempo real, atraso é pior que perda; o UDP não retransmite e mantém o fluxo. D e</mark> E descrevem o UDP incorretamente. 

**Resposta. Alternativa C.** 

**QUESTÃO COMENTADA 2** 

**Enunciado.** Analise as afirmações sobre comunicação e concorrência: 

I. Um socket é identificado pela combinação de endereço IP e porta. 

II. Em um servidor sequencial, um cliente lento pode bloquear o atendimento dos demais. 

III. Uma condição de corrida só ocorre em sistemas com mais de uma máquina. 

<mark>IV. A exclusão mútua na seção crítica evita resultados imprevisíveis no acesso a dado</mark> compartilhado. 

<mark>É correto o que se afirma em:</mark> 

- **(A)** I e III. 

**(B)** II e III. 

**(C)** I, II e IV. 

**(D)** III e IV. 

- **<mark>(E)</mark>** <mark>I, II, III e IV.</mark> 

**<mark>Resolução.</mark>** <mark>I, II e IV são corretas. III é falsa: a condição de corrida ocorre entre threads na mesma</mark> máquina, não exige várias máquinas. 

**Resposta. Alternativa C.** 

**QUESTÃO COMENTADA 3** 

**Enunciado.** Avalie a asserção e a razão a seguir. 

<mark>ASSERÇÃO: É seguro reenviar automaticamente uma requisição idempotente que não obteve</mark> resposta. 

PORQUE 

RAZÃO: Uma operação idempotente, repetida, leva ao mesmo estado final. 

<mark>A respeito dessas afirmações, assinale a opção correta:</mark> 

**(A)** A asserção e a razão são verdadeiras, e a razão justifica a asserção. 

- **(B)** A asserção e a razão são verdadeiras, mas a razão não justifica a asserção. 

- **(C)** A asserção é verdadeira e a razão é falsa. 

- **(D)** A asserção é falsa e a razão é verdadeira. 

- **<mark>(E)</mark>** <mark>A asserção e a razão são falsas.</mark> 

**<mark>Resolução.</mark>** <mark>Ambas são verdadeiras e a razão explica a asserção: é justamente por levar ao mesmo</mark> estado final que a operação idempotente pode ser retentada com segurança. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**Resposta. Alternativa A.** 

**QUESTÃO COMENTADA 4** 

**<mark>Enunciado.</mark>** <mark>Uma equipe precisa de comunicação interna de alto volume entre microsserviços, com contrato tipado e baixa sobrecarga de dados na rede. A tecnologia mais adequada é:</mark> 

- **(A)** SOAP com XML. 

- **(B)** gRPC com Protocol Buffers. 

- **(C)** REST sobre JSON, exclusivamente. 

- **(D)** Troca de arquivos por FTP. 

- **<mark>(E)</mark>** <mark>Mensagens por e-mail.</mark> 

**<mark>Resolução.</mark>** <mark>O gRPC oferece contrato tipado (.proto), serialização binária compacta e HTTP/2,</mark> ideal para comunicação interna de alto volume entre serviços. 

**Resposta. Alternativa B.** 

###### **QUESTÃO COMENTADA 5** 

**<mark>Enunciado.</mark>** <mark>Um servidor sequencial trava o atendimento quando um cliente demora a responder. A técnica que permite atender vários clientes simultaneamente, sem que um bloqueie os outros, é:</mark> 

- **(A)** Reduzir o tamanho do buffer. 

- **(B)** Usar uma thread por conexão aceita. 

- **(C)** Trocar TCP por UDP. 

- **(D)** Diminuir o número da porta. 

- **<mark>(E)</mark>** <mark>Desativar o registro de log.</mark> 

**<mark>Resolução.</mark>** <mark>Atribuir uma thread a cada conexão libera o laço principal para aceitar o próximo</mark> cliente; um cliente lento afeta apenas a sua própria thread. 

**<mark>Resposta. Alternativa B.</mark>** 

###### **EM RESUMO** 

Do byte no socket até um serviço de IA publicado: esta foi a Verificação C1. 

<mark>Se você responde estas 6 com segurança, está pronto para a C1.A1.</mark> 

###### ◆ **FOCO ENADE** 

<mark>A prova C1.A1 integra todo o bloco. No ENADE, os temas de comunicação (</mark> **<mark>socket</mark>** <mark>,</mark> **<mark>TCP/UDP</mark>** <mark>, RPC/RMI,</mark> **<mark>REST</mark>** <mark>) e de concorrência (</mark> **<mark>thread</mark>** <mark>) aparecem quase sempre combinados em estudos de</mark> caso — treine a leitura do cenário antes de escolher a alternativa. 

**<mark>Costuma cair:</mark>** <mark>Todo o conteúdo da Verificação C1 é cobrado de forma integrada.; Comunicação entre processos: sockets, TCP/UDP, RPC/RMI e REST.; Concorrência, threads e exclusão mútua.;</mark> Arquiteturas cliente-servidor e orientada a serviços. 

**<mark>Termos-chave:</mark>** <mark>Socket · TCP/UDP · Thread · RPC/gRPC · REST · Inferência</mark> 

**GLOSSÁRIO DO CAPÍTULO** 

**C1.A1** Avaliação escrita individual, estilo ENADE, valendo 5,0 pontos. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**C1.A2** Trabalho prático entregue no repositório, valendo 5,0 pontos. **<mark>Rubrica</mark>** <mark>Tabela que define como os pontos do trabalho são distribuídos.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**PARTE C2** 

## **Coordenação e consistência** 

Aulas 8 a 12 

_Como coordenar máquinas que falham e que não compartilham um relógio. Mensageria, relógios lógicos, teorema CAP, consenso com Raft e padrões de resiliência._ 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 8  ·  C2  ·  24/09/2026** 

#### **Mensageria, eventos e API Gateway** 

**Neste capítulo você vai aprender a:** 

- Diferenciar comunicação síncrona de assíncrona e saber quando usar cada uma. 

- Processar inferências de IA de forma assíncrona com fila e worker. 

- Explicar o papel de um API Gateway numa arquitetura de microsserviços. 

###### **Síncrono contra assíncrono** 

Na comunicação síncrona, o cliente faz a chamada e fica esperando a resposta; é simples, mas ele trava enquanto espera. Na assíncrona, o cliente entrega a tarefa, recebe imediatamente um comprovante (um identificador) e vai buscar o resultado depois. Para uma inferência de IA que leva segundos, segurar o cliente é um desperdício e um convite a problemas — se muitos clientes esperam ao mesmo tempo, o serviço satura. A comunicação assíncrona resolve isso ao quebrar o vínculo temporal entre o pedido e o processamento. 

###### **A fila como amortecedor e o desacoplamento** 

O mecanismo por trás do assíncrono é a **fila** de mensagens. Um **produtor** coloca a tarefa na fila; um **worker** (o consumidor) a retira e processa. A palavra-chave aqui é **desacoplamento** : quem produz não precisa saber quem consome, nem quando, nem quantos consumidores existem. Esse desacoplamento traz dois benefícios enormes. O primeiro é a absorção de picos: se chegam mais pedidos do que a capacidade de processamento, eles se acumulam na fila em vez de derrubar o serviço. O segundo é a escalabilidade simples: para dar conta de mais carga, basta subir mais workers consumindo a mesma fila, sem mudar quem produz. 

Mas e quando o processamento falha? Uma tarefa pode dar erro — uma entrada inválida, uma dependência fora do ar. A boa prática é reprocessar algumas vezes e, persistindo a falha, encaminhar a mensagem para uma fila de descarte, a **dead-letter** . Em vez de tentar para sempre (travando o worker) ou simplesmente perder a mensagem, a dead-letter a isola para análise posterior, mantendo o fluxo principal saudável. 

Uma variação importante é o modelo publicar/assinar, ou **pub/sub** : enquanto na fila cada mensagem é consumida por um único worker, no pub/sub a mesma mensagem é entregue a todos os interessados. É a base da arquitetura orientada a eventos, muito usada em nuvem — um pedido concluído pode, ao mesmo tempo, atualizar o estoque, notificar o cliente e alimentar um relatório. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

###### **API Gateway: a porta única** 

Quando o sistema passa a ter vários serviços, o cliente não deve conhecer o endereço de cada um. O **API Gateway** resolve isso sendo a porta de entrada única: ele recebe todas as requisições e as encaminha ao serviço certo, além de centralizar o que é comum a todos — autenticação, limite de requisições e registro de log. É também no gateway que aplicaremos a segurança, mais adiante. Um cuidado relacionado é o versionamento: acrescentar um campo novo a uma resposta é seguro, mas remover ou renomear um campo quebra os clientes existentes e exige publicar uma nova versão da API (por exemplo, /v2), mantendo a antiga no ar durante a transição. 

**NO SEU TRABALHO — C2.A2: RAG Distribuído em Microsserviços** 

<mark>Começa o</mark> **<mark>C2.A2 — RAG Distribuído em Microsserviços</mark>** <mark>. A mensageria desta aula é a espinha do trabalho: ao menos uma etapa do fluxo deve passar por fila.</mark> 

- Clonar o repositório `sd-2026-2-kit-c2a2` . 

- TAREFA 4 — mensageria: novo worker + `docker-compose.yml` . 

- <mark>Iniciar o serviço de ingestão/embeddings.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c2a2_ 

###### **EM RESUMO** 

Síncrono: espero a resposta. Assíncrono: recebo um protocolo e busco o resultado depois. A fila absorve picos de carga e desacopla quem pede de quem processa. 

Fila: um consumidor por mensagem. Pub/sub: vários interessados na mesma mensagem. 

<mark>O gateway é a porta única: o cliente fala com ele, e ele fala com os serviços.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Cobrança típica: comunicação síncrona versus assíncrona, o papel do middleware orientado a mensagens (MOM), a diferença entre</mark> **<mark>fila</mark>** <mark>e</mark> **<mark>pub/sub</mark>** <mark>, os papéis de</mark> **<mark>produtor</mark>** <mark>e</mark> **<mark>worker</mark>** <mark>, o</mark> **<mark>desacoplamento</mark>** <mark>e o uso de</mark> **<mark>dead-letter</mark>** <mark>para falhas. Microsserviços,</mark> **<mark>API Gateway</mark>** <mark>e</mark> versionamento de contratos também são recorrentes. 

**<mark>Costuma cair:</mark>** <mark>Comunicação síncrona e assíncrona entre processos.; Middleware orientado a mensagens (MOM), filas e pub/sub.; Arquitetura orientada a eventos e desacoplamento.;</mark> Microsserviços, API Gateway e versionamento de contratos. 

**<mark>Termos-chave:</mark>** <mark>Fila · Produtor · Worker · Pub/sub · Dead-letter · API Gateway · Versionamento</mark> 

###### **QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Sobre a diferença entre uma fila de trabalho e o modelo publicar/assinar (pub/sub), assinale a alternativa correta.</mark> 

- **(A)** Na fila as mensagens são descartadas; em pub/sub, persistidas. 

- **<mark>(B)</mark>** <mark>Na fila, cada mensagem é consumida por um único consumidor; em pub/sub, a mesma</mark> mensagem é entregue a todos os assinantes interessados. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

- **(C)** A fila exige consistência forte e o pub/sub, consistência eventual. 

**(D)** A fila só funciona com UDP e o pub/sub, apenas com TCP. 

**<mark>(E)</mark>** <mark>Não há diferença prática entre os dois modelos.</mark> 

**<mark>Resolução.</mark>** <mark>A fila distribui trabalho (um consumidor por mensagem); o pub/sub distribui</mark> informação (vários assinantes recebem a mesma mensagem). 

**Resposta. Alternativa B.** 

**GLOSSÁRIO DO CAPÍTULO** 

**Fila** Estrutura que guarda tarefas até que um consumidor as processe. 

**Worker** Processo que retira mensagens da fila e as executa. 

**Pub/sub** Modelo em que uma mensagem publicada chega a vários assinantes. 

**Dead-letter** Fila de descarte para mensagens que falharam repetidamente. 

**<mark>API Gateway</mark>** <mark>Serviço que recebe todas as requisições e as encaminha aos serviços internos.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 9  ·  C2  ·  01/10/2026** 

#### **Tempo e ordenação: relógios lógicos** 

**Neste capítulo você vai aprender a:** 

- Explicar por que não existe relógio global confiável em sistemas distribuídos. 

- Aplicar relógios de Lamport para ordenar eventos. 

- Usar relógios vetoriais para identificar eventos concorrentes. 

###### **Por que não existe um 'agora' comum** 

Cada máquina tem seu próprio relógio, e dois relógios nunca marcam exatamente o mesmo instante — eles andam em ritmos ligeiramente diferentes, um fenômeno chamado **clock drift** (desvio de relógio). Sincronizá-los pela rede não resolve o problema de vez, porque a própria mensagem de sincronização leva um tempo variável para chegar. A consequência prática é séria: você não pode confiar em carimbo de hora para decidir a ordem em que eventos aconteceram em máquinas diferentes. Se dois pedidos chegam quase juntos a servidores distintos, comparar os relógios físicos pode inverter a ordem real dos fatos. 

###### **Relógio de Lamport** 

A saída é abandonar a hora real e ordenar por **causalidade** — a relação em que um evento influenciou a ocorrência de outro. O **relógio lógico** de **Lamport** faz isso com um contador por processo. A cada evento local, o contador aumenta em 1. Ao enviar uma mensagem, o processo manda junto o valor atual do seu contador. Ao receber, o destinatário adota o maior entre o próprio contador e o valor recebido, e soma 1. Essa regra — máximo mais um — garante uma propriedade essencial, chamada 'aconteceu antes': se um evento A causou um evento B, então o número de A é menor que o de B. Atenção, porém: a recíproca não vale — um número menor não prova, sozinho, que houve relação de causa. 

###### **Relógio vetorial e eventos concorrentes** 

Para saber com certeza se dois eventos têm relação de causa ou se são **eventos concorrentes** (independentes, sem que um tenha influenciado o outro), usa-se o **relógio vetorial** : em vez de um único número, cada processo mantém um vetor com um contador para cada processo do sistema. Comparando dois vetores posição a posição, é possível determinar três situações: um evento causou o outro (um vetor é menor ou igual em todas as posições), o inverso, ou os eventos são concorrentes (cada vetor é maior em alguma posição, sem dominar o outro). Essa capacidade de detectar concorrência é a base para 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

identificar conflitos entre réplicas — assunto do próximo capítulo, quando duas cópias de um dado são escritas ao mesmo tempo. 

###### **NO SEU TRABALHO — C2.A2: RAG Distribuído em Microsserviços** 

<mark>O serviço de recuperação compara a pergunta com os documentos por similaridade. A teoria de ordenação desta aula reforça um cuidado: a recuperação deve depender do conteúdo, não da hora de cada máquina.</mark> 

**<mark>•</mark>** <mark>TAREFA 2 — busca por similaridade no serviço de recuperação.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c2a2_ 

###### **EM RESUMO** 

Não existe relógio global confiável: por isso ordenamos por causalidade, não por hora. 

Lamport garante que causa vem antes do efeito, mas não distingue eventos concorrentes. 

<mark>O relógio vetorial diz se um evento causou o outro ou se ambos são concorrentes.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Tema clássico e frequentemente mal estudado. Saiba calcular o valor de um</mark> **<mark>relógio lógico</mark>** <mark>de</mark> **<mark>Lamport</mark>** <mark>após envio e recebimento (a regra do máximo mais um) e saiba interpretar um</mark> **<mark>relógio vetorial</mark>** <mark>para classificar dois eventos como causais ou</mark> **<mark>concorrentes</mark>** <mark>. Termos:</mark> **<mark>clock drift</mark>** <mark>,</mark> **causalidade** , relação 'aconteceu antes'. 

**<mark>Costuma cair:</mark>** <mark>Sincronização de relógios físicos e desvio (clock drift).; Relógios lógicos de Lamport e relação</mark> ' <mark>aconteceu antes</mark> ' <mark>.; Relógios vetoriais e detecção de concorrência.; Ordenação de</mark> eventos e exclusão mútua distribuída. 

**<mark>Termos-chave:</mark>** <mark>Relógio lógico · Lamport · Relógio vetorial · Causalidade · Eventos concorrentes · Clock drift</mark> 

###### **QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>No processo P1, um evento leva seu relógio de Lamport a 3. P1 então envia uma mensagem a P2 com o carimbo 3. No recebimento, o relógio de P2 valia 7. Após o recebimento, o relógio de P2 passa a valer:</mark> 

**(A)** 3. **(B)** 7. **(C)** 8. **(D)** 10. **<mark>(E)</mark>** <mark>4.</mark> 

**<mark>Resolução.</mark>** <mark>A regra de Lamport no recebimento é máximo(relógio local, carimbo) + 1 = máximo(7,</mark> 3) + 1 = 8. 

**Resposta. Alternativa C.** 

###### **GLOSSÁRIO DO CAPÍTULO** 

**Relógio lógico** Contador que ordena eventos sem depender da hora real. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**Lamport** Algoritmo de relógio lógico baseado em um contador por processo. **Relógio vetorial** Vetor de contadores que permite detectar eventos concorrentes. **Causalidade** Relação em que um evento influenciou a ocorrência de outro. **<mark>Eventos concorrentes</mark>** <mark>Eventos sem relação de causa entre si.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 10  ·  C2  ·  08/10/2026** 

#### **Replicação, consistência e o teorema CAP** 

**Neste capítulo você vai aprender a:** 

- Explicar por que replicamos dados e qual problema isso cria. 

- Enunciar o teorema CAP e aplicá-lo a decisões de projeto. 

- Diferenciar consistência forte de consistência eventual. 

###### **Por que replicar e qual o preço** 

**Replicação** é manter cópias do mesmo dado em máquinas diferentes. Faz-se isso por dois motivos: disponibilidade, para que o sistema continue respondendo se uma cópia cair; e desempenho, para que leituras sejam mais rápidas e mais próximas do usuário. O preço é manter todas as cópias iguais, o que é difícil sobretudo quando há escritas simultâneas em réplicas diferentes — e é justamente aí que entra o problema da concorrência distribuída que os relógios vetoriais ajudam a detectar. 

###### **O teorema CAP** 

O **teorema CAP** formaliza um limite fundamental. Das três propriedades desejáveis — Consistência (toda leitura enxerga a escrita mais recente), Disponibilidade (todo pedido recebe resposta) e tolerância a **Partição de rede** (o sistema continua mesmo se a rede se dividir em grupos que não se comunicam) — não é possível garantir as três ao mesmo tempo quando há partição. E como partições de rede acontecem de fato, na prática o P não é opcional. O teorema, portanto, não é uma escolha de dois entre três feita no papel: é uma decisão concreta, tomada durante a falha, entre responder de forma consistente (recusando pedidos que não pode garantir) ou responder sempre (arriscando devolver dado desatualizado). 

###### **Consistência forte, eventual e convergência** 

Essa decisão se traduz em dois modelos. Na **consistência forte** , depois que você escreve, toda leitura vê o valor novo — o que exige coordenação entre as réplicas e custa tempo. Na **consistência eventual** , as cópias podem divergir por um instante e só depois se acertam; nesse intervalo, uma leitura pode devolver dado antigo. O processo pelo qual as réplicas divergentes voltam a coincidir, sem intervenção externa, chama-se **convergência** : passado o período de propagação (e resolvidos eventuais conflitos), todas as cópias chegam ao mesmo valor. A escolha do modelo é do projeto, não da tecnologia, e precisa ser justificada pelo caso de uso: um saldo bancário exige consistência forte, pois divergir 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

significaria permitir dois saques do mesmo dinheiro; já um contador de curtidas ou de visualizações tolera perfeitamente a consistência eventual, porque um número momentaneamente desatualizado não causa prejuízo. 

**NO SEU TRABALHO — C2.A2: RAG Distribuído em Microsserviços** 

<mark>O índice vetorial do seu RAG é um dado replicável: pensar em consistência ajuda a decidir o que acontece se ele for atualizado durante uma consulta.</mark> 

- TAREFA 1 — persistir o índice para não perdê-lo ao reiniciar. 

- <mark>Definir a consistência aceitável para o índice.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c2a2_ 

**EM RESUMO** 

Replicar dá disponibilidade e desempenho, mas cria o problema de manter as cópias iguais. Durante uma partição de rede, você escolhe: ou responde certo, ou responde sempre. <mark>Dado crítico pede consistência forte; o resto costuma aceitar consistência eventual.</mark> 

###### ◆ **FOCO ENADE** 

<mark>O</mark> **<mark>teorema CAP</mark>** <mark>é dos temas mais cobrados. Saiba enunciá-lo e, principalmente, aplicá-lo: dado um cenário com</mark> **<mark>partição de rede</mark>** <mark>, indicar se sacrificar</mark> **<mark>consistência forte</mark>** <mark>ou disponibilidade, e justificar. Os conceitos de</mark> **<mark>replicação</mark>** <mark>,</mark> **<mark>consistência eventual</mark>** <mark>e</mark> **<mark>convergência</mark>** <mark>, além de bancos</mark> distribuídos e particionamento (sharding), completam o tópico. 

**<mark>Costuma cair:</mark>** <mark>Replicação de dados: objetivos e estratégias.; Teorema CAP e suas implicações de projeto.; Modelos de consistência: forte, eventual e causal.; Bancos de dados distribuídos e</mark> particionamento (sharding). 

**<mark>Termos-chave:</mark>** <mark>Replicação · Teorema CAP · Partição de rede · Consistência forte · Consistência eventual · Convergência</mark> 

**QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>De acordo com o teorema CAP, diante de uma partição de rede, um sistema distribuído precisa escolher entre:</mark> 

- **(A)** Consistência e tolerância a partição. 

- **(B)** Consistência e disponibilidade. 

- **(C)** Disponibilidade e tolerância a partição. 

- **(D)** Latência e vazão. 

- **<mark>(E)</mark>** <mark>Replicação e particionamento.</mark> 

**<mark>Resolução.</mark>** <mark>Como a partição (P) é inevitável durante a falha, a escolha real, naquele momento, é</mark> entre responder de forma consistente (C) ou permanecer disponível (A). 

**Resposta. Alternativa B.** 

**GLOSSÁRIO DO CAPÍTULO** 

**Replicação** Manter cópias do mesmo dado em máquinas diferentes. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**Teorema CAP** Durante uma partição, é preciso escolher entre consistência e disponibilidade. **Partição de rede** Falha em que o sistema fica dividido em grupos que não se comunicam. **Consistência forte** Toda leitura enxerga a escrita mais recente. **<mark>Consistência eventual</mark>** <mark>As cópias convergem para o mesmo valor depois de algum tempo.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 11  ·  C2  ·  22/10/2026** 

#### **Consenso (Raft) e resiliência** 

**Neste capítulo você vai aprender a:** 

- Explicar o problema do consenso e como o Raft o resolve. 

- Aplicar tempo-limite, retentativa com espera progressiva e disjuntor. 

- Explicar por que a idempotência é essencial quando há retentativa. 

###### **O problema do consenso** 

**Consenso** é fazer várias máquinas concordarem sobre um mesmo valor, mesmo diante de falhas. Ele aparece sempre que o sistema precisa de uma decisão única e coerente: quem é o líder, qual a ordem das operações, o que foi de fato confirmado. É difícil porque mensagens atrasam, se perdem e máquinas caem sem avisar. Um resultado teórico famoso, o FLP, mostra que num sistema totalmente assíncrono não existe algoritmo que garanta consenso em todos os casos — por isso, na prática, os algoritmos usam tempo-limite para contornar o impasse e seguir em frente. 

###### **Como o Raft funciona** 

O **Raft** é um algoritmo de consenso projetado para ser compreensível. Cada máquina é seguidor, candidato ou líder. Se um seguidor fica sem notícia do líder por um tempo, ele se torna candidato e pede votos; quem receber votos da maioria vira o novo líder. Essa maioria tem nome: **quórum** — o número mínimo de máquinas (mais da metade) necessário para tomar uma decisão. Exigir quórum é o que impede a existência de dois líderes ao mesmo tempo, pois duas maiorias não podem coexistir. A partir daí, toda operação passa pelo líder, que a registra no seu **log replicado** e a copia para os seguidores; quando a maioria confirma o registro, a operação é considerada efetivada. É esse mecanismo que sustenta sistemas como o etcd, por trás do Kubernetes. 

###### **Projetar contando com a falha** 

Do lado prático, resiliência é o conjunto de padrões que mantêm o sistema de pé quando uma dependência falha. Três são essenciais. Toda chamada de rede precisa de um **tempolimite** — sem ele, uma chamada travada segura o serviço para sempre. A retentativa ajuda em falhas passageiras, mas deve usar espera progressiva (backoff), aumentando o intervalo a cada tentativa, para não piorar a sobrecarga do serviço que já está sofrendo. E o **circuit breaker** (disjuntor) abre após várias falhas seguidas, passando a recusar chamadas na hora; depois de um tempo, deixa passar uma chamada de teste para ver se o serviço voltou. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

Isso evita a **falha em cascata** — o efeito dominó em que um serviço quebrado, por acúmulo de chamadas travadas, derruba todos os que dependem dele. 

Um detalhe amarra resiliência e REST: só é seguro retentar operações idempotentes. A **idempotência** , que vimos no estilo REST, é o que garante que repetir uma chamada não produza efeito duplicado. Se você retenta algo que não é idempotente, corre o risco de executá-lo duas vezes — uma cobrança dobrada, por exemplo. A solução prática é o cliente enviar um identificador único que o servidor usa para reconhecer e ignorar repetições. 

**NO SEU TRABALHO — C2.A2: RAG Distribuído em Microsserviços** 

<mark>A chamada ao LLM é a dependência externa lenta e instável do RAG — exatamente o caso do</mark> **<mark>circuit breaker</mark>** <mark>desta aula.</mark> 

**<mark>•</mark>** <mark>TAREFA 3 — circuit breaker na chamada ao LLM, com tempo-limite e retentativa.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c2a2_ 

**EM RESUMO** 

Consenso é fazer várias máquinas concordarem apesar de falhas e atrasos. 

O Raft elege um líder por maioria e só confirma o que a maioria registrou. 

Toda chamada tem tempo-limite; toda retentativa tem espera; o disjuntor corta o que já caiu. <mark>Só é seguro retentar aquilo que é idempotente.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Dois eixos numa aula só. Do consenso:</mark> **<mark>Raft</mark>** <mark>, eleição de líder,</mark> **<mark>quórum</mark>** <mark>/maioria e</mark> **<mark>log replicado</mark>** <mark>. Da resiliência e dependabilidade: tipos de falha,</mark> **<mark>tempo-limite</mark>** <mark>,</mark> **<mark>circuit breaker</mark>** <mark>,</mark> **<mark>falha em cascata</mark>** <mark>e</mark> **<mark>idempotência</mark>** <mark>. Ambos são muito cobrados; a idempotência costuma aparecer ligada a</mark> retentativa. 

**<mark>Costuma cair:</mark>** <mark>Problema do consenso, eleição de líder e quórum.; Tolerância a falhas por replicação de máquina de estados.; Tipos de falha, dependabilidade e mecanismos de recuperação.;</mark> Padrões de resiliência e degradação controlada. 

**<mark>Termos-chave:</mark>** <mark>Consenso · Raft · Quórum / maioria · Log replicado · Tempo-limite · Circuit breaker · Idempotência</mark> 

**QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Em um cluster que utiliza o algoritmo Raft com 5 nós, o número mínimo de nós disponíveis e em acordo para eleger um líder e confirmar operações é:</mark> 

**(A)** 1. **(B)** 2. **(C)** 3. **(D)** 4. **<mark>(E)</mark>** <mark>5.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**<mark>Resolução.</mark>** <mark>O Raft opera por quórum, que é a maioria. Em 5 nós, a maioria é 3 — o que impede que</mark> duas partes do cluster elejam líderes diferentes. **Resposta. Alternativa C. GLOSSÁRIO DO CAPÍTULO Consenso** Fazer várias máquinas concordarem sobre um valor apesar de falhas. **Raft** Algoritmo de consenso baseado em eleição de líder e log replicado. **Quórum** Número mínimo de máquinas (maioria) necessário para decidir. **Circuit breaker** Padrão que interrompe chamadas a um serviço que está falhando. **Idempotência** Propriedade de operação que, repetida, mantém o mesmo resultado. **<mark>Falha em cascata</mark>** <mark>Falha que se propaga de um serviço para os demais.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 12  ·  C2  ·  29/10/2026** 

#### **Revisão e Avaliação C2.A1 + entrega do C2.A2** 

**Neste capítulo você vai aprender a:** 

- Revisar de forma consolidada os conceitos da Verificação C2. 

- Realizar a avaliação escrita C2.A1, no estilo ENADE (5,0 pontos). 

- Entregar o trabalho prático C2.A2 (5,0 pontos). 

###### **O que amarra o bloco de coordenação** 

A segunda verificação responde a uma pergunta mais profunda que a primeira: como coordenar máquinas que falham e que não compartilham um relógio? Vimos que a **fila** e a comunicação assíncrona desacoplam e absorvem carga; que os relógios de **Lamport** e vetoriais ordenam eventos sem depender da hora real; que o teorema **CAP** impõe uma escolha durante partições; que o **Raft** permite concordar por maioria; e que padrões como o **circuit breaker** e a **idempotência** mantêm o sistema de pé. Foi neste bloco que você construiu o RAG — a técnica de Retrieval-Augmented Generation, em que o sistema recupera trechos de documentos e os fornece a um LLM para gerar uma resposta fundamentada. São os conceitos mais abstratos do semestre e, não por acaso, os mais valorizados pelo ENADE. 

**NO SEU TRABALHO — C2.A2: RAG Distribuído em Microsserviços** 

<mark>Dia de entrega do C2.A2. Feche o fluxo de ponta a ponta e documente a arquitetura dos três serviços.</mark> 

- TAREFA 5 — fluxo completo: pergunta entra, resposta fundamentada sai. 

- TAREFA 6 — README com diagrama dos três serviços. 

- <mark>Conferir a rubrica e entregar.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c2a2_ 

###### **Questões comentadas (estilo ENADE)** 

_Questões novas, elaboradas para esta disciplina e inspiradas nos temas e formatos das provas reais do ENADE de Computação (edições 2021 e 2024)._ 

###### **QUESTÃO COMENTADA 1** 

**<mark>Enunciado.</mark>** <mark>No processo P1 um evento leva seu relógio de Lamport a 5. P1 envia uma mensagem a P2 com o carimbo 5; no recebimento, o relógio de P2 valia 2. Após o recebimento, o relógio de P2 é:</mark> 

- **(A)** 2. **(B)** 5. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**(C)** 6. **(D)** 7. **<mark>(E)</mark>** <mark>3.</mark> 

**<mark>Resolução.</mark>** <mark>máximo(2, 5) + 1 = 6. Aqui é o carimbo recebido (5) que</mark> ' <mark>puxa</mark> ' <mark>o valor, por ser maior</mark> que o relógio local (2). 

**Resposta. Alternativa C.** 

**QUESTÃO COMENTADA 2** 

**<mark>Enunciado.</mark>** <mark>Um sistema de reserva de assentos de avião, replicado em dois data centers, sofre uma partição de rede entre eles. À luz do teorema CAP, a decisão mais adequada é:</mark> 

**(A)** Sacrificar a tolerância a partição. 

- **<mark>(B)</mark>** <mark>Sacrificar a disponibilidade, mantendo a consistência, para não vender o mesmo assento</mark> duas vezes. 

**(C)** Sacrificar a consistência, permitindo vendas nos dois lados. 

**(D)** Sacrificar simultaneamente consistência e disponibilidade. 

**<mark>(E)</mark>** <mark>Não é possível decidir sem mais informações.</mark> 

**<mark>Resolução.</mark>** <mark>Com a partição em curso, resta escolher entre C e A. Permitir vendas nos dois lados</mark> geraria overbooking; sacrifica-se a disponibilidade para preservar a consistência. 

**Resposta. Alternativa B.** 

**QUESTÃO COMENTADA 3** 

**<mark>Enunciado.</mark>** <mark>Um cluster usa o Raft com 5 nós. Qual o número mínimo de nós disponíveis e em acordo para eleger um líder e confirmar operações?</mark> 

**(A)** 1. **(B)** 2. **(C)** 3. **(D)** 4. **<mark>(E)</mark>** <mark>5.</mark> 

**<mark>Resolução.</mark>** <mark>O Raft opera por quórum (maioria). Em 5 nós, a maioria é 3, o que impede a existência</mark> de dois líderes simultâneos. 

**Resposta. Alternativa C.** 

**QUESTÃO COMENTADA 4** 

**Enunciado.** Analise as afirmações sobre replicação e consistência: 

I. Replicar dados pode aumentar a disponibilidade e reduzir a latência de leitura. 

II. Na consistência forte, uma leitura logo após a escrita sempre enxerga o valor novo. 

III. Na consistência eventual, as réplicas nunca chegam a convergir. IV. Manter réplicas idênticas é trivial quando há escritas concorrentes. <mark>É correto o que se afirma em:</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**(A)** I e II. 

**(B)** I, II e IV. 

**(C)** II e III. 

**(D)** I e IV. 

**<mark>(E)</mark>** <mark>III e IV.</mark> 

**<mark>Resolução.</mark>** <mark>I e II são corretas. III é falsa: na consistência eventual as réplicas convergem após um</mark> tempo. IV é falsa: manter réplicas iguais sob escrita concorrente é difícil. 

**Resposta. Alternativa A.** 

**QUESTÃO COMENTADA 5** 

**Enunciado.** Avalie a asserção e a razão a seguir. 

<mark>ASSERÇÃO: Processar inferências de IA de forma assíncrona, por fila, melhora a resiliência do</mark> serviço sob picos de carga. 

PORQUE 

<mark>RAZÃO: A fila desacopla o produtor do consumidor e absorve picos, acumulando tarefas em vez de</mark> derrubar o serviço. 

<mark>A respeito dessas afirmações, assinale a opção correta:</mark> 

- **(A)** A asserção e a razão são verdadeiras, e a razão justifica a asserção. 

- **(B)** A asserção e a razão são verdadeiras, mas a razão não justifica a asserção. 

- **(C)** A asserção é verdadeira e a razão é falsa. 

- **(D)** A asserção é falsa e a razão é verdadeira. 

- **<mark>(E)</mark>** <mark>A asserção e a razão são falsas.</mark> 

**<mark>Resolução.</mark>** <mark>Ambas são verdadeiras e a razão explica a asserção: é o desacoplamento e a absorção</mark> de picos pela fila que tornam o serviço mais resiliente. 

**<mark>Resposta. Alternativa A.</mark>** 

**EM RESUMO** 

A C2 responde a uma pergunta: como coordenar máquinas que falham e não compartilham relógio? 

<mark>Se você responde estas 6 com segurança, está pronto para a C2.A1.</mark> 

###### ◆ **FOCO ENADE** 

<mark>A prova C2.A1 cobra este bloco em nível operacional — o que acontece com o sistema — e não em demonstração formal. É exatamente o recorte que o ENADE costuma adotar:</mark> **<mark>fila</mark>** <mark>,</mark> **<mark>Lamport</mark>** <mark>,</mark> **<mark>CAP</mark>** <mark>,</mark> **Raft** , **circuit breaker** e **idempotência** aplicados a cenários. 

**<mark>Costuma cair:</mark>** <mark>Todo o conteúdo da Verificação C2 é cobrado de forma integrada.; Comunicação assíncrona, filas e arquitetura orientada a eventos.; Relógios lógicos, replicação, consistência, CAP e</mark> consenso.; Tolerância a falhas e padrões de resiliência. 

**<mark>Termos-chave:</mark>** <mark>Fila · Lamport · CAP · Raft · Circuit breaker · Idempotência</mark> 

**GLOSSÁRIO DO CAPÍTULO** 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**C2.A1** Avaliação escrita individual, estilo ENADE, valendo 5,0 pontos. **C2.A2** Trabalho prático RAG distribuído, valendo 5,0 pontos. **<mark>RAG</mark>** <mark>Geração de resposta apoiada em documentos recuperados por busca vetorial.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**PARTE C3** 

## **Nuvem, implantação e segurança** 

Aulas 13 a 17 

_Como colocar e manter um sistema distribuído no ar. Containers, nuvem, serverless, observabilidade, segurança e LGPD._ 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 13  ·  C3  ·  05/11/2026** 

#### **Computação em nuvem, containers e o primeiro deploy** 

**Neste capítulo você vai aprender a:** 

- Diferenciar os modelos de serviço IaaS, PaaS, SaaS e FaaS. 

- Explicar o que é um container e por que ele resolve o 'na minha máquina funciona'. 

- Publicar o seu serviço de IA em nuvem, com URL pública. 

###### **Os modelos de serviço em nuvem** 

A computação em nuvem se organiza em camadas de responsabilidade. No **IaaS** (Infraestrutura como Serviço) você aluga a máquina e cuida de todo o resto — sistema operacional, atualizações, aplicação. No **PaaS** (Plataforma como Serviço) você entrega apenas o código e a plataforma cuida de executá-lo; Render e Railway são exemplos. No **SaaS** (Software como Serviço) você apenas usa um software pronto, como o Gmail. E no **FaaS** (Função como Serviço) você entrega uma função que roda somente quando é chamada. Quanto mais adiante nessa lista, menos infraestrutura você gerencia — e menos controle detém. A escolha certa depende de quanto controle o seu caso exige e de quanta operação você quer evitar. 

###### **Elasticidade e custo** 

A característica que define a nuvem é a **elasticidade** : a capacidade de crescer e encolher a quantidade de recursos conforme a demanda, automaticamente. É isso que a distingue de um servidor alugado de tamanho fixo, que fica ocioso na baixa e insuficiente no pico. Como a cobrança na nuvem é pelo uso, uma decisão de arquitetura vira diretamente uma decisão de custo — um serviço que não libera recursos ociosos, ou que faz trabalho desnecessário, aparece na fatura. Pensar em custo passou a fazer parte da engenharia, prática hoje chamada de FinOps. 

###### **Containers: o fim do 'na minha máquina funciona'** 

O **container** empacota o código junto com suas dependências e configuração, de modo que o serviço roda igual na sua máquina, na do colega e na nuvem. Vale distinguir dois termos que costumam se confundir: a **imagem** é o molde imutável que você constrói, e o container é a execução daquela imagem — uma imagem pode gerar muitos containers idênticos. A receita que descreve como construir a imagem é o **Dockerfile** , um arquivo de texto com os passos (a partir de qual base, quais dependências instalar, qual comando executar). Diferente de uma máquina virtual, que carrega um sistema operacional 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

completo, o container compartilha o núcleo do sistema hospedeiro — por isso é muito mais leve e sobe em segundos, e não em minutos. 

**NO SEU TRABALHO — C3.A2: Plataforma de IA como Serviço** 

<mark>Começa o</mark> **<mark>C3.A2 — Plataforma de IA como Serviço</mark>** <mark>, o projeto integrador. Hoje você conteineriza os serviços e faz o primeiro deploy.</mark> 

- Clonar o repositório `sd-2026-2-kit-c3a2` . 

- TAREFA 3 — um Dockerfile por serviço. 

- <mark>TAREFA 5 — primeiro deploy em nuvem free tier.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c3a2_ 

###### **EM RESUMO** 

IaaS entrega máquina; PaaS entrega plataforma; SaaS entrega software; FaaS entrega execução. Nuvem é elástica e cobra pelo uso: decisão de arquitetura vira decisão de custo. <mark>A imagem empacota o ambiente inteiro: acaba o</mark> ' <mark>na minha máquina funciona</mark> ' <mark>.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Nuvem é um eixo garantido. Domine os modelos de serviço (</mark> **<mark>IaaS</mark>** <mark>,</mark> **<mark>PaaS</mark>** <mark>,</mark> **<mark>SaaS</mark>** <mark>,</mark> **<mark>FaaS</mark>** <mark>) e de implantação (pública, privada, híbrida), o conceito de</mark> **<mark>elasticidade</mark>** <mark>e a diferença entre</mark> virtualização por máquina virtual e por **container** — com os termos **imagem** e **Dockerfile** . 

**<mark>Costuma cair:</mark>** <mark>Modelos de serviço em nuvem: IaaS, PaaS, SaaS e FaaS.; Modelos de implantação: nuvem pública, privada e híbrida.; Elasticidade, escalabilidade e economia de escala.; Virtualização</mark> e containers: diferenças e vantagens. 

**<mark>Termos-chave:</mark>** <mark>IaaS · PaaS · SaaS · FaaS · Elasticidade · Container · Imagem · Dockerfile</mark> 

###### **QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Uma empresa quer publicar sua aplicação entregando apenas o código-fonte, sem gerenciar sistema operacional nem provisionar servidores. O modelo de serviço em nuvem adequado é:</mark> 

**(A)** IaaS. 

- **(B)** PaaS. 

**(C)** SaaS. 

**(D)** Instalação local (on-premise). 

**<mark>(E)</mark>** <mark>Colocation.</mark> 

**<mark>Resolução.</mark>** <mark>Em PaaS o cliente entrega o código e a plataforma cuida de executá-lo, incluindo o</mark> sistema operacional. O IaaS ainda exigiria gerenciar o SO; o SaaS é software pronto. 

**Resposta. Alternativa B.** 

###### **GLOSSÁRIO DO CAPÍTULO** 

**IaaS** Modelo em que se contrata infraestrutura (máquinas, rede, disco). 

**PaaS** Modelo em que se entrega o código e a plataforma cuida da execução. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**FaaS** Modelo em que se entrega uma função executada sob demanda. **Elasticidade** Capacidade de crescer e encolher conforme a demanda. **Imagem** Molde imutável com aplicação, dependências e configuração. **<mark>Container</mark>** <mark>Instância em execução de uma imagem.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 14  ·  C3  ·  12/11/2026** 

#### **Orquestração, serverless e computação na borda** 

**Neste capítulo você vai aprender a:** 

- Subir um sistema de vários containers com um único comando. 

- Explicar descoberta de serviços e o papel de um orquestrador como o Kubernetes. 

- Explicar o modelo serverless, o cold start e a computação na borda. 

###### **Orquestração: de containers a sistema** 

Ter os containers prontos não basta: é preciso subi-los, conectá-los e ordená-los — isso é **orquestração** . Subir cada um à mão é lento e propenso a erro, e os serviços precisam se encontrar apesar de o IP mudar a cada execução. O **Docker Compose** descreve todo o sistema num único arquivo e o sobe com um comando; os containers ficam numa rede interna e se localizam pelo nome do serviço — a forma mais simples de **descoberta de serviços** , o mecanismo pelo qual um serviço encontra o endereço de outro sem precisar de IPs fixos. Quando uma máquina só não basta, entra o **Kubernetes** , que distribui containers por um conjunto de máquinas, reinicia o que cai, cria réplicas e faz balanceamento de carga automaticamente. Nesta disciplina você usa Compose e entende o conceito de Kubernetes, sem precisar operá-lo. 

###### **Serverless e seus limites** 

No modelo **serverless** você publica uma função e ela executa quando um evento a dispara; se não há chamadas, nada roda e nada é cobrado, e a escala é automática. Existe servidor, sim — a diferença é que você não o gerencia. O preço é o **cold start** — a primeira chamada após um período parado é mais lenta, porque a plataforma precisa provisionar o ambiente — e os limites de tempo e memória por execução. Por isso o serverless brilha em cargas intermitentes e é inadequado para processos longos e contínuos, que pedem um container sempre de pé. 

###### **Computação na borda** 

A computação na borda — **edge computing** — executa o código perto do usuário, e não num data center distante, com o objetivo direto de reduzir a **latência** , já que a distância física custa tempo. Essa ideia se apoia na **CDN** (Content Delivery Network), uma rede de servidores espalhados geograficamente que guardam cópias de conteúdo próximas de quem acessa. Um padrão comum é ler na borda e escrever na origem: aproveita-se a 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

proximidade para validação, cache e filtragem, deixando para o centro apenas o que realmente precisa ser centralizado. 

**NO SEU TRABALHO — C3.A2: Plataforma de IA como Serviço** 

<mark>A orquestração desta aula é o que faz o sistema inteiro subir com um único comando.</mark> 

- TAREFA 4 — `docker-compose` completo, subindo todos os serviços juntos. 

- <mark>Opcional: um componente serverless ou na borda.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c3a2_ 

###### **EM RESUMO** 

Compose orquestra em uma máquina; Kubernetes orquestra em um conjunto delas. Serverless: você publica a função; a nuvem cuida de executar e escalar. 

Serverless é ótimo para carga intermitente; ruim para processo longo e contínuo. 

<mark>Na borda o código roda perto do usuário, cortando latência.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Cobrança frequente:</mark> **<mark>orquestração</mark>** <mark>de containers, escalabilidade horizontal,</mark> **<mark>descoberta de serviços</mark>** <mark>e balanceamento de carga (com</mark> **<mark>Docker Compose</mark>** <mark>e</mark> **<mark>Kubernetes</mark>** <mark>). O modelo</mark> **<mark>serverless</mark>** <mark>, o</mark> **<mark>cold start</mark>** <mark>, a arquitetura orientada a eventos e a computação na borda (</mark> **<mark>edge</mark> computing** , **CDN** , IoT) aparecem como 'tecnologias emergentes'. 

**<mark>Costuma cair:</mark>** <mark>Orquestração de containers e escalabilidade horizontal.; Descoberta de serviços e balanceamento de carga.; Modelo FaaS, computação sem servidor e arquitetura orientada a</mark> eventos.; Computação na borda, CDN e Internet das Coisas. 

**<mark>Termos-chave:</mark>** <mark>Orquestração · Docker Compose · Kubernetes · Descoberta de serviços · Serverless · Cold start · Edge computing · CDN</mark> 

**QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Sobre o modelo serverless (FaaS), assinale a alternativa correta.</mark> 

**(A)** Não existe servidor algum envolvido na execução. 

**(B)** A função executa sob demanda e não é cobrada quando ociosa, ao custo de cold start. 

**(C)** É o modelo ideal para processos longos e contínuos. 

**(D)** Elimina a necessidade de qualquer conexão de rede. 

**<mark>(E)</mark>** <mark>Garante consistência forte entre réplicas.</mark> 

**<mark>Resolução.</mark>** <mark>O serverless executa por evento, cobra pelo uso e sofre cold start; por isso é</mark> inadequado a processos longos e contínuos, que pedem um container sempre de pé. 

**Resposta. Alternativa B.** 

###### **GLOSSÁRIO DO CAPÍTULO** 

**Orquestração** Coordenar a execução de vários containers como um sistema só. 

**Kubernetes** Orquestrador que distribui containers por um conjunto de máquinas. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**Descoberta de serviços** Mecanismo pelo qual um serviço encontra o endereço de outro. **Serverless** Modelo em que se publicam funções sem gerenciar servidores. **Cold start** Atraso da primeira execução após um período de inatividade. **<mark>Edge computing</mark>** <mark>Execução de código próximo ao usuário para reduzir latência.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 15  ·  C3  ·  19/11/2026** 

#### **Observabilidade: enxergar o que acontece no sistema** 

**Neste capítulo você vai aprender a:** 

- Diferenciar log, métrica e rastreamento (trace). 

- Explicar por que rastreamento distribuído é indispensável em microsserviços. 

- Instrumentar o seu sistema e seguir uma requisição de ponta a ponta. 

###### **Os três pilares da observabilidade** 

Operar um sistema distribuído exige enxergar o que acontece dentro dele, e isso se apoia em três pilares. O **log** é o registro textual do que ocorreu em um ponto do código — útil para saber o que aconteceu, mas isolado. A **métrica** é um número agregado ao longo do tempo, como requisições por segundo ou latência média — útil para enxergar tendências e disparar alertas. E o **trace** (rastreamento) reconstrói o caminho completo de uma única requisição atravessando vários serviços. Sem os três, a depuração vira adivinhação: o log conta o que houve num ponto, a métrica mostra a tendência geral, mas só o trace liga os pontos. 

###### **Por que o rastreamento distribuído é indispensável** 

Num sistema de um serviço só, o log basta para achar o problema. Mas quando uma requisição passa pelo gateway, entra numa fila, é processada por um worker e chama um LLM externo, ela percorre quatro lugares — e o log isolado de cada um não conta a história completa. O rastreamento distribuído amarra todas as etapas por meio de um identificador de **correlação** : um mesmo código único acompanha a requisição por todos os serviços, permitindo descobrir exatamente em qual trecho o tempo foi gasto e onde está o **gargalo** — o ponto mais lento, que limita o desempenho de todo o fluxo. 

###### **OpenTelemetry como padrão** 

O **OpenTelemetry** se tornou o padrão aberto para instrumentar aplicações, independente de fornecedor: você instrumenta o código uma vez e envia os dados para a ferramenta de análise que preferir, sem ficar preso a um produto específico. A lição de projeto é que instrumentar faz parte do desenvolvimento, e não algo que se improvisa depois que o incidente já aconteceu — quem só pensa em observabilidade durante a crise descobre, tarde demais, que não tem os dados para entender o que houve. 

**NO SEU TRABALHO — C3.A2: Plataforma de IA como Serviço** 

<mark>Observabilidade é requisito do trabalho: sem rastreamento, você não sabe onde o sistema é lento.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

###### **<mark>•</mark>** <mark>TAREFA 7 — rastreamento distribuído cobrindo gateway → fila → worker.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c3a2_ 

###### **EM RESUMO** 

Log conta o que houve; métrica mostra a tendência; rastreamento mostra o caminho. 

O rastreamento amarra as etapas de uma requisição por um identificador comum. 

<mark>OpenTelemetry padroniza a instrumentação e evita amarrar você a um fornecedor.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Observabilidade conecta-se a monitoramento, gerenciamento e desempenho de sistemas distribuídos, e às práticas de DevOps. Distinga os três pilares —</mark> **<mark>log</mark>** <mark>,</mark> **<mark>métrica</mark>** <mark>e</mark> **<mark>trace</mark>** <mark>— e domine a</mark> ideia de **correlação** de eventos, de identificação de **gargalo** e do padrão **OpenTelemetry** . 

**<mark>Costuma cair:</mark>** <mark>Monitoramento, gerenciamento e desempenho de sistemas distribuídos.; Rastreamento distribuído e correlação de eventos.; Métricas de qualidade de serviço: latência, vazão</mark> e disponibilidade.; Práticas de DevOps e operação de serviços. 

**<mark>Termos-chave:</mark>** <mark>Log · Métrica · Trace / rastreamento · OpenTelemetry · Correlação · Gargalo</mark> 

###### **QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Uma requisição atravessa quatro serviços e apresenta lentidão intermitente. Para descobrir em qual etapa o tempo é consumido, o recurso de observabilidade mais adequado é:</mark> 

- **(A)** Ler o log isolado de cada serviço. 

**(B)** Acompanhar a métrica agregada de uso de CPU. 

**(C)** O rastreamento distribuído (trace), que correlaciona as etapas por um identificador comum. 

- **(D)** Aumentar o detalhamento do log apenas no gateway. 

**<mark>(E)</mark>** <mark>Substituir os containers por máquinas virtuais.</mark> 

**<mark>Resolução.</mark>** <mark>Apenas o rastreamento reconstrói o caminho de uma requisição entre serviços e revela</mark> em qual trecho está o gargalo. 

**Resposta. Alternativa C.** 

###### **GLOSSÁRIO DO CAPÍTULO** 

**Log** Registro textual de um evento ocorrido no código. 

**Métrica** Valor numérico agregado e acompanhado ao longo do tempo. 

**Trace** Registro do caminho completo de uma requisição entre serviços. 

**OpenTelemetry** Padrão aberto de instrumentação de aplicações. 

**<mark>Correlação</mark>** <mark>Identificador comum que liga as etapas de uma mesma requisição.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 16  ·  C3  ·  Estudo Dirigido (EAD)** 

#### **Segurança, LGPD e revisão geral para o ENADE** 

**Neste capítulo você vai aprender a:** 

- Aplicar criptografia, TLS e autenticação com JWT. 

- Reconhecer as obrigações da LGPD num pipeline que processa dados pessoais. 

- Revisar de forma integrada os temas de sistemas distribuídos cobrados no ENADE. 

###### **Criptografia: o essencial para usar bem** 

Você não precisa implementar algoritmos, mas precisa saber escolher. A **criptografia simétrica** usa a mesma chave para cifrar e decifrar: é rápida, ideal para grandes volumes, mas exige que as duas partes combinem a chave com antecedência e em segredo. A **criptografia assimétrica** usa um par de chaves, uma pública e uma privada: o que uma cifra, só a outra decifra — o que resolve o problema da troca inicial da chave, porém é mais lenta. E o **hash** é um resumo de tamanho fixo e de mão única: serve para verificar integridade (se o dado mudou, o resumo muda) e para guardar senhas, mas não para cifrar, pois não há como reverter. Na prática, os sistemas combinam as três: assimétrica para acertar com segurança uma chave de sessão, simétrica para cifrar o tráfego, hash para garantir integridade — é exatamente assim que o TLS opera. 

###### **TLS, autenticação e autorização** 

O **TLS/HTTPS** — o 'S' do HTTPS — cifra o tráfego e comprova a identidade do servidor por meio de um certificado digital. Sobre ele, dois conceitos que costumam ser confundidos: a autenticação responde 'quem é você', enquanto a autorização responde 'o que você pode fazer'. O **JWT** (JSON Web Token) é um token assinado que carrega a identidade do usuário e pode ser verificado pela própria assinatura, sem consultar o banco a cada requisição. E o princípio de **Zero Trust** estabelece que nada é confiável só por estar na rede interna: todo pedido é autenticado e autorizado, como se viesse de fora. 

###### **LGPD e anonimização no pipeline de IA** 

Dado pessoal é qualquer informação que identifique alguém, direta ou indiretamente, e a **LGPD** (Lei Geral de Proteção de Dados) impõe princípios claros: finalidade declarada e coleta do mínimo necessário. Num pipeline de IA há um cuidado específico: o texto enviado a uma API de LLM sai da sua infraestrutura e vai para um terceiro. Daí a importância da **anonimização** — remover ou mascarar, antes do envio, os elementos que identificam a pessoa (nome, CPF, e-mail), de modo que o dado deixe de ser pessoal. Some a isso jamais 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

registrar dado pessoal em log e definir um prazo de retenção. Ignorar essas medidas não é apenas má engenharia — é descumprimento legal, com sanções previstas em lei. 

###### **Preparação final para o ENADE** 

Esta aula acontece na véspera do ENADE. Vale um sobrevoo por todo o semestre: comunicação (sockets, TCP/UDP, RPC/RMI, REST, SOAP), concorrência, coordenação (relógios, consenso, quórum), dados (replicação, CAP, consistência), nuvem (modelos de serviço, containers, virtualização) e segurança (criptografia, TLS, autenticação, LGPD). O melhor roteiro de revisão é reler todos os quadros EM RESUMO e todas as caixas FOCO ENADE deste livro, além das QUESTÕES COMENTADAS dos capítulos 7, 12 e 17. 

**NO SEU TRABALHO — C3.A2: Plataforma de IA como Serviço** 

<mark>Segurança e LGPD fecham a parte técnica do projeto integrador.</mark> 

- TAREFA 1 — autenticação JWT no gateway. 

- TAREFA 2 — limite de requisições (rate limit). 

- TAREFA 8 — HTTPS no serviço publicado. 

- <mark>TAREFA 9 — seção de conformidade LGPD no README.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c3a2_ 

**EM RESUMO** 

Assimétrica acerta a chave; simétrica transporta os dados; hash garante integridade. TLS protege o caminho; autenticação identifica; autorização define o permitido. 

Colete o mínimo, declare a finalidade e não vaze dado pessoal em log nem para o LLM. 

<mark>O ENADE cobra os fundamentos: leia os quadros</mark> ' <mark>EM RESUMO</mark> ' <mark>de todas as 15 aulas anteriores.</mark> 

###### ◆ **FOCO ENADE** 

<mark>Segurança da informação é eixo próprio no exame:</mark> **<mark>criptografia simétrica</mark>** <mark>,</mark> **<mark>assimétrica</mark>** <mark>e</mark> **<mark>hash</mark>** <mark>;</mark> **<mark>TLS/HTTPS</mark>** <mark>e certificados; autenticação, autorização,</mark> **<mark>JWT</mark>** <mark>e</mark> **<mark>Zero Trust</mark>** <mark>; e</mark> **<mark>LGPD</mark>** <mark>, com seus princípios de finalidade e necessidade e o recurso da</mark> **<mark>anonimização</mark>** <mark>. Questões de ética e legislação</mark> são comuns. 

**<mark>Costuma cair:</mark>** <mark>Criptografia simétrica, assimétrica e funções de hash.; Protocolos seguros: TLS/HTTPS e certificados digitais.; Autenticação, autorização e controle de acesso.; LGPD,</mark> privacidade e proteção de dados pessoais. 

**<mark>Termos-chave:</mark>** <mark>Criptografia simétrica · Criptografia assimétrica · Hash · TLS/HTTPS · JWT · Zero Trust · LGPD · Anonimização</mark> 

**QUESTÃO DE AUTOAVALIAÇÃO (estilo ENADE)** 

**<mark>Enunciado.</mark>** <mark>Um sistema de RAG envia trechos de documentos com dados pessoais a uma API pública de LLM. À luz da LGPD, a medida mais adequada é:</mark> 

- **(A)** Ampliar o tempo-limite da requisição. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**<mark>(B)</mark>** <mark>Anonimizar os dados pessoais antes do envio e restringir o tratamento à finalidade</mark> declarada. 

- **(C)** Aumentar o número de réplicas do serviço. 

**(D)** Converter a comunicação de REST para gRPC. 

- **<mark>(E)</mark>** <mark>Armazenar os dados pessoais também nos logs, para auditoria.</mark> 

**<mark>Resolução.</mark>** <mark>Aplicam-se os princípios da finalidade e da necessidade (mínimo necessário);</mark> anonimiza-se antes do envio. Gravar dado pessoal em log agrava a exposição. 

**Resposta. Alternativa B.** 

**GLOSSÁRIO DO CAPÍTULO** 

**Criptografia simétrica** Usa a mesma chave para cifrar e decifrar. 

**Criptografia assimétrica** Usa um par de chaves, pública e privada. 

**Hash** Resumo de mão única usado para verificar integridade. 

**TLS** Protocolo que cifra a comunicação e autentica o servidor. 

**JWT** Token assinado que carrega a identidade do usuário. 

**<mark>LGPD</mark>** <mark>Lei brasileira de proteção de dados pessoais.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**AULA 17  ·  C3  ·  26/11/2026** 

#### **Avaliação C3.A1, entrega do C3.A2 e tendências** 

**Neste capítulo você vai aprender a:** 

- Revisar de forma consolidada os conceitos da Verificação C3. 

- Realizar a avaliação escrita C3.A1, no estilo ENADE (5,0 pontos). 

- Entregar o projeto integrador C3.A2 (5,0 pontos) e conhecer as tendências da área. 

###### **O semestre inteiro em uma página** 

Vale olhar para trás e ver o caminho. O bloco C1 respondeu como dois programas conversam: sockets, gRPC, REST e a IA como serviço. O bloco C2 respondeu como coordenar máquinas que falham: filas, relógios lógicos, CAP, Raft e resiliência. O bloco C3 respondeu como colocar e manter tudo isso no ar: **containers** , nuvem, **orquestração** , **observabilidade** , **TLS/JWT** e **LGPD** . Do primeiro socket ao sistema publicado, você construiu, do zero, uma plataforma distribuída de IA — que vale mais em uma entrevista de emprego do que muitos certificados. 

###### **Para onde a área está indo** 

Encerramos com as tendências que devem moldar os próximos anos. A arquitetura orientada a eventos consolida-se como padrão de integração em nuvem. Serverless e borda continuam crescendo, movidos pela lógica de processar perto do usuário e pagar só pelo uso. O **data mesh** propõe uma mudança de organização: em vez de um time central dono de todos os dados, cada domínio (vendas, estoque, pagamentos) trata os seus dados como um produto, com dono e contrato próprios. E os sistemas **AI-native** são aqueles concebidos com a inteligência artificial no centro da arquitetura, e não como um recurso acrescentado depois. Zero Trust e observabilidade, por fim, deixaram de ser diferenciais e passaram a requisitos padrão de qualquer sistema sério. 

**NO SEU TRABALHO — C3.A2: Plataforma de IA como Serviço** 

<mark>Dia de entrega do projeto integrador C3.A2 — material de portfólio. Finalize a resiliência e o relatório de trade-offs.</mark> 

- TAREFA 6 — resiliência (tempo-limite, retentativa, circuit breaker). 

- TAREFA 10 — relatório de trade-offs (CAP, custo, latência). 

- <mark>Conferir a URL pública no ar e entregar.</mark> 

**Repositório do kit:** _sd-2026-2-kit-c3a2_ 

###### **Questões comentadas (estilo ENADE)** 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

_Questões novas, elaboradas para esta disciplina e inspiradas nos temas e formatos das provas reais do ENADE de Computação (edições 2021 e 2024)._ 

###### **QUESTÃO COMENTADA 1** 

**Enunciado.** Analise as afirmações sobre modelos de computação em nuvem, segundo o NIST: <mark>I. No SaaS, o usuário utiliza aplicações executadas na infraestrutura do provedor, sem gerenciar a</mark> infraestrutura subjacente. 

<mark>II. No IaaS, o cliente provisiona processamento, armazenamento e rede, e gerencia o sistema</mark> operacional. 

III. No PaaS, o cliente é responsável por manter o hardware físico do data center. 

IV. A elasticidade permite ajustar os recursos conforme a demanda. 

<mark>É correto o que se afirma em:</mark> 

**(A)** I e III. **(B)** I, II e IV. **(C)** II e III. **(D)** III e IV. **<mark>(E)</mark>** <mark>I, II, III e IV.</mark> 

**<mark>Resolução.</mark>** <mark>I, II e IV são corretas. III é falsa: em qualquer modelo de nuvem, é o provedor — e não</mark> o cliente — que mantém o hardware físico. 

**Resposta. Alternativa B.** 

**QUESTÃO COMENTADA 2** 

**Enunciado.** Analise as afirmações sobre mecanismos criptográficos em uma comunicação segura: <mark>I. A criptografia assimétrica pode ser usada para estabelecer com segurança a chave simétrica da</mark> sessão. 

II. Uma função de hash como o SHA-256 permite verificar a integridade dos dados. 

III. A criptografia simétrica dispensa qualquer segredo compartilhado. 

IV. O TLS combina criptografia assimétrica e simétrica. 

<mark>É correto o que se afirma em:</mark> 

**(A)** I e III. **(B)** II e III. **(C)** I, II e IV. **(D)** I e IV. **<mark>(E)</mark>** <mark>I, II, III e IV.</mark> 

**<mark>Resolução.</mark>** <mark>I, II e IV são corretas. III é falsa: a criptografia simétrica depende de uma chave secreta</mark> compartilhada entre as partes. 

**Resposta. Alternativa C.** 

**QUESTÃO COMENTADA 3** 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

- **<mark>Enunciado.</mark>** <mark>Assinale a alternativa correta sobre a diferença entre containers e máquinas virtuais.</mark> **(A)** O container inclui um sistema operacional completo, o que o torna mais pesado que a VM. **<mark>(B)</mark>** <mark>O container compartilha o núcleo do sistema operacional hospedeiro, sendo mais leve e de</mark> inicialização mais rápida que a VM. 

   - **(C)** A máquina virtual dispensa hipervisor, ao contrário do container. 

   - **(D)** Container e máquina virtual são termos equivalentes. 

   - **<mark>(E)</mark>** <mark>O container não permite empacotar as dependências da aplicação.</mark> 

**<mark>Resolução.</mark>** <mark>O container virtualiza no nível do sistema operacional e compartilha o kernel; a VM</mark> virtualiza o hardware e carrega um SO completo, sendo mais pesada. 

**Resposta. Alternativa B.** 

**QUESTÃO COMENTADA 4** 

**<mark>Enunciado.</mark>** <mark>Uma requisição atravessa gateway, fila, worker e uma API externa, com lentidão intermitente. Para localizar em qual etapa o tempo é gasto, o recurso mais adequado é:</mark> 

- **(A)** O log isolado de cada serviço. 

- **(B)** A métrica agregada de uso de CPU. 

- **(C)** O rastreamento distribuído, correlacionando as etapas por um identificador comum. 

- **(D)** Aumentar o número de réplicas. 

- **<mark>(E)</mark>** <mark>Substituir os containers por máquinas virtuais.</mark> 

**<mark>Resolução.</mark>** <mark>Somente o rastreamento distribuído reconstrói o percurso da requisição e aponta o</mark> gargalo; log e métrica, isolados, não fazem isso. 

**Resposta. Alternativa C.** 

**QUESTÃO COMENTADA 5** 

**Enunciado.** Avalie a asserção e a razão a seguir. 

<mark>ASSERÇÃO: Antes de enviar textos de clientes a uma API pública de LLM, deve-se anonimizar os</mark> dados pessoais. 

PORQUE 

<mark>RAZÃO: A LGPD estabelece os princípios da finalidade e da necessidade, limitando o tratamento ao</mark> mínimo necessário para a finalidade declarada. 

<mark>A respeito dessas afirmações, assinale a opção correta:</mark> 

- **(A)** A asserção e a razão são verdadeiras, e a razão justifica a asserção. 

- **(B)** A asserção e a razão são verdadeiras, mas a razão não justifica a asserção. 

- **(C)** A asserção é verdadeira e a razão é falsa. 

**(D)** A asserção é falsa e a razão é verdadeira. 

- **<mark>(E)</mark>** <mark>A asserção e a razão são falsas.</mark> 

**<mark>Resolução.</mark>** <mark>Ambas são verdadeiras e a razão justifica a asserção: é para atender aos princípios da</mark> finalidade e da necessidade que se anonimiza o dado antes de enviá-lo a terceiros. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

**<mark>Resposta. Alternativa A.</mark>** 

**EM RESUMO** A C3 transformou o seu protótipo local em um sistema publicado, observável e seguro. De um socket na Aula 2 a uma plataforma de IA em nuvem na Aula 17. <mark>O futuro próximo combina eventos, borda, dados como produto e IA no centro da arquitetura.</mark> 

###### ◆ **FOCO ENADE** 

<mark>A prova C3.A1 integra nuvem,</mark> **<mark>containers</mark>** <mark>,</mark> **<mark>orquestração</mark>** <mark>, serverless,</mark> **<mark>observabilidade</mark>** <mark>e segurança (</mark> **<mark>TLS/JWT</mark>** <mark>,</mark> **<mark>LGPD</mark>** <mark>). Some a consciência das tendências (eventos, borda,</mark> **<mark>data mesh</mark>** <mark>,</mark> **AI-native** ): questões de 'panorama' recompensam quem enxerga o quadro completo. **<mark>Costuma cair:</mark>** <mark>Todo o conteúdo da Verificação C3 é cobrado de forma integrada.; Computação em nuvem, containers e orquestração.; Serverless, borda e arquitetura orientada a eventos.; Segurança</mark> da informação, criptografia e LGPD. 

**<mark>Termos-chave:</mark>** <mark>IaaS/PaaS/SaaS/FaaS · Container · Orquestração · Observabilidade · TLS/JWT · LGPD</mark> 

**GLOSSÁRIO DO CAPÍTULO C3.A1** Avaliação escrita individual, estilo ENADE, valendo 5,0 pontos. **C3.A2** Projeto integrador entregue no repositório, valendo 5,0 pontos. **Data mesh** Abordagem em que cada domínio é dono de seus dados, tratados como produto. **<mark>AI-native</mark>** <mark>Sistema concebido com a IA como parte central da arquitetura.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

### **Apêndice A — Mapa de revisão para o ENADE** 

O ENADE 2026 (29 de novembro) inclui os cursos de Análise e Desenvolvimento de Sistemas, Ciência da Computação e Sistemas de Informação. A tabela abaixo reúne, capítulo a capítulo, os temas com maior probabilidade de aparecer e os termos-chave correspondentes. Use-a como roteiro final de revisão. 

|**Aula**|**Temas cobrados no ENADE**|**Termos-chave**|
|---|---|---|
|**1**|Conceito e caracterização de sistemas distribuídos.;<br>Vantagens e desafios: escalabilidade, disponibilidade e<br>falha parcial.; Diferença entre sistema centralizado e<br>sistema distribuído.; Tipos de transparência (acesso,<br>localização, replicação).|Sistema distribuído · Falha parcial ·<br>Transparência · Escalabilidade · Latência|
|**2**|Modelo cliente-servidor comparado ao modelo P2P.;<br>Características de TCP e UDP e critério para escolher<br>entre eles.; Conceito de socket, porta e<br>endereçamento.; Camadas do modelo TCP/IP e<br>encapsulamento.|Cliente-servidor · P2P · Socket · Porta ·<br>TCP · UDP|
|**3**|Concorrência e paralelismo: diferença entre os dois.;<br>Condição de corrida, exclusão mútua e seção crítica.;<br>Threads e processos: quando usar cada um.;<br>Escalabilidade de servidores e gargalos.|Thread · Condição de corrida · Exclusão<br>mútua · Seção crítica · Lock · Bloqueante|
|**4**|Conceito de RPC e transparência de acesso.; RMI e<br>invocação de métodos remotos.; Serialização e<br>representação de dados na rede.; Middleware de<br>comunicação e stubs.|RPC · RMI · gRPC · Protocol Buffers ·<br>Stub · Serialização · Middleware|
|**5**|Web services: SOAP e REST, diferenças e<br>aplicabilidade.; Verbos HTTP, códigos de status e<br>idempotência.; Arquitetura orientada a serviços (SOA)<br>e interoperabilidade.; Contratos de API e<br>documentação (WSDL, OpenAPI).|REST · SOAP · Recurso · Verbo HTTP ·<br>Código de status · OpenAPI ·<br>Idempotência|
|**6**|Aplicações e casos de uso de sistemas distribuídos.;<br>Arquitetura de serviços e separação de<br>responsabilidades.; Desempenho, latência e tempo de<br>resposta em serviços.; Tecnologias emergentes:<br>inteligência artificial como serviço.|Inferência · Modelo · Embedding · Token<br>· LLM · Cold start|
|**7**|Todo o conteúdo da Verificação C1 é cobrado de forma<br>integrada.; Comunicação entre processos: sockets,<br>TCP/UDP, RPC/RMI e REST.; Concorrência, threads e<br>exclusão mútua.; Arquiteturas cliente-servidor e|Socket · TCP/UDP · Thread · RPC/gRPC ·<br>REST · Inferência|



Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

||orientada a serviços.||
|---|---|---|
|**8**|Comunicação síncrona e assíncrona entre processos.;<br>Middleware orientado a mensagens (MOM), filas e<br>pub/sub.; Arquitetura orientada a eventos e<br>desacoplamento.; Microsserviços, API Gateway e<br>versionamento de contratos.|Fila · Produtor · Worker · Pub/sub ·<br>Dead-letter · API Gateway ·<br>Versionamento|
|**9**|Sincronização de relógios físicos e desvio (clock drift).;<br>Relógios lógicos de Lamport e relação 'aconteceu<br>antes'.; Relógios vetoriais e detecção de concorrência.;<br>Ordenação de eventos e exclusão mútua distribuída.|Relógio lógico · Lamport · Relógio<br>vetorial · Causalidade · Eventos<br>concorrentes · Clock drift|
|**10**|Replicação de dados: objetivos e estratégias.; Teorema<br>CAP e suas implicações de projeto.; Modelos de<br>consistência: forte, eventual e causal.; Bancos de dados<br>distribuídos e particionamento (sharding).|Replicação · Teorema CAP · Partição de<br>rede · Consistência forte · Consistência<br>eventual · Convergência|
|**11**|Problema do consenso, eleição de líder e quórum.;<br>Tolerância a falhas por replicação de máquina de<br>estados.; Tipos de falha, dependabilidade e<br>mecanismos de recuperação.; Padrões de resiliência e<br>degradação controlada.|Consenso · Raft · Quórum / maioria · Log<br>replicado · Tempo-limite · Circuit<br>breaker · Idempotência|
|**12**|Todo o conteúdo da Verificação C2 é cobrado de forma<br>integrada.; Comunicação assíncrona, filas e arquitetura<br>orientada a eventos.; Relógios lógicos, replicação,<br>consistência, CAP e consenso.; Tolerância a falhas e<br>padrões de resiliência.|Fila · Lamport · CAP · Raft · Circuit<br>breaker · Idempotência|
|**13**|Modelos de serviço em nuvem: IaaS, PaaS, SaaS e<br>FaaS.; Modelos de implantação: nuvem pública,<br>privada e híbrida.; Elasticidade, escalabilidade e<br>economia de escala.; Virtualização e containers:<br>diferenças e vantagens.|IaaS · PaaS · SaaS · FaaS · Elasticidade ·<br>Container · Imagem · Dockerfile|
|**14**|Orquestração de containers e escalabilidade<br>horizontal.; Descoberta de serviços e balanceamento de<br>carga.; Modelo FaaS, computação sem servidor e<br>arquitetura orientada a eventos.; Computação na<br>borda, CDN e Internet das Coisas.|Orquestração · Docker Compose ·<br>Kubernetes · Descoberta de serviços ·<br>Serverless · Cold start · Edge computing ·<br>CDN|
|**15**<br>**16**|Monitoramento, gerenciamento e desempenho de<br>sistemas distribuídos.; Rastreamento distribuído e<br>correlação de eventos.; Métricas de qualidade de<br>serviço: latência, vazão e disponibilidade.; Práticas de<br>DevOps e operação de serviços.<br>Criptografia simétrica, assimétrica e funções de hash.;|Log · Métrica · Trace / rastreamento ·<br>OpenTelemetry · Correlação · Gargalo<br>Criptografia simétrica · Criptografia|



Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

||Protocolos seguros: TLS/HTTPS e certificados digitais.;<br>Autenticação, autorização e controle de acesso.; LGPD,<br>privacidade e proteção de dados pessoais.|assimétrica · Hash · TLS/HTTPS · JWT ·<br>Zero Trust · LGPD · Anonimização|
|---|---|---|
|**17**|Todo o conteúdo da Verificação C3 é cobrado de forma<br>integrada.; Computação em nuvem, containers e<br>orquestração.; Serverless, borda e arquitetura<br>orientada a eventos.; Segurança da informação,<br>criptografia e LGPD.|IaaS/PaaS/SaaS/FaaS · Container ·<br>Orquestração · Observabilidade ·<br>TLS/JWT · LGPD|



###### ◆ **DICA DE PROVA** 

<mark>Os temas de sistemas distribuídos quase nunca vêm isolados no ENADE: eles aparecem em estudos de caso que combinam comunicação, coordenação e nuvem. Treine primeiro a leitura do cenário e só então escolha a alternativa. As três provas A1 da disciplina seguem esse mesmo formato, justamente para prepará-lo.</mark> 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

### **Apêndice B — Bibliografia e materiais de apoio** 

###### **Básica** 

- COULOURIS, G.; DOLLIMORE, J.; KINDBERG, T. Sistemas Distribuídos: conceitos e projeto. 5. ed. Porto Alegre: Bookman, 2012. 

KLEPPMANN, M. Designing Data-Intensive Applications. O'Reilly, 2017. 

TANENBAUM, A. S.; VAN STEEN, M. Distributed Systems. 4. ed., 2023 (PDF gratuito dos autores). 

###### **Complementar** 

NEWMAN, S. Building Microservices. 2. ed. O'Reilly, 2021. 

RICHARDSON, C. Microservices Patterns. Manning, 2018. 

BURNS, B. Designing Distributed Systems. O'Reilly, 2018. 

Documentação oficial: gRPC, FastAPI, Docker, OpenTelemetry e do provedor de nuvem adotado. 

###### **Materiais abertos** 

MIT 6.824 — Distributed Systems (aulas e laboratórios abertos). 

- Concurrent and Distributed Systems — University of Cambridge, Martin Kleppmann (notas e vídeos). 

Provas e gabaritos do ENADE de Computação (INEP) — edições de 2021 e 2024. 

Sistemas Distribuídos e Computação em Nuvem · FAESA 2026/2 

