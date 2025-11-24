#!/bin/sh

while true
do
    echo "=== Rodando TESTE LEVE ==="
    k6 run /scripts/teste_leve.js
    echo "Aguardando 5 segundos..."
    sleep 5

    echo "=== Rodando TESTE MÉDIO ==="
    k6 run /scripts/teste_medio.js
    echo "Aguardando 5 segundos..."
    sleep 5

    echo "=== Rodando TESTE PESADO ==="
    k6 run /scripts/teste_pesado.js
    echo "Aguardando 5 segundos..."
    sleep 5

    echo "=== Rodando TESTE DE STRESS ==="
    k6 run /scripts/teste_de_stress.js
    echo "Aguardando 5 segundos..."
    sleep 5

    echo "=== CICLO COMPLETO — Reiniciando ==="
done
