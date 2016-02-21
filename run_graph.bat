set DATA_FILENAME=data.json
set GRAPH_FILENAME=out.png
pypy create_run_data.py %DATA_FILENAME% SphereIndividual SphereAggregatedIndividual
python create_fitness_graph.py %DATA_FILENAME% %GRAPH_FILENAME%
