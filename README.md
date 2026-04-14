# Automotive Market Intelligence Portal

Pare de tentar adivinhar o mercado usando médias mentirosas no Excel. Este portal separa o sinal do ruído usando engenharia de verdade e estatística aplicada, sem firulas.

# Arquitetura
O projeto foi modularizado para ser escalável. Se você gosta de scripts monolíticos e bagunçados, este repositório não é para você.

```python
Market_Intel/
├── data/               # Onde os dados brutos moram
├── src/                # O cérebro da operação
│   ├── engine.py       # Motor de ETL (limpeza e carga)
│   └── intelligence.py # Modelagem estatística e ML
├── app.py              # Interface para quem não lê código
└── requirements.txt    # Onde o 'na minha máquina funciona' morre
```

# O que tem por baixo do capô
* SPC (Statistical Process Control): Monitoramento de estabilidade via limites 3-Sigma. Saiu da linha? É anomalia, não flutuação comum.
* Consistência (BoxPlot): Tratamento de zero-filling para expor quem tem volume real e quem vive de picos desesperados de fim de mês.
* Inteligência Preditiva: Árvore de Decisão do Scikit-Learn que identifica se o que manda no share é o calendário ou a região.

## Como rodar (Se você tiver o mínimo de competência)
Copie e execute uma linha por vez. O uso de # permite que você copie o bloco todo sem quebrar o terminal.

```bash
# Clone o repositório
git clone https://github.com/belaskco/market_intel.git
# Entre na pasta (O passo que você provavelmente ia esquecer)
cd market_intel
# Instale as dependências
pip install -r requirements.txt
# Execute a aplicação
streamlit run app.py
```

# Considerações
Matemática aplicada ao caos automotivo. Se o código for útil, ótimo. Se encontrar um bug, sinta-se à vontade para consertar e abrir um Pull Request — ou continue reclamando no LinkedIn.

### Desenvolvido por Cassio de Andrade.
https://www.linkedin.com/in/cassioandrade84/