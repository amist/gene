set DATA_FILENAME=data.json
set GRAPH_FILENAME=out.png
set CONFIG_FILENAME=runs.config
pypy create_run_data_new.py %DATA_FILENAME% %CONFIG_FILENAME% 
python create_fitness_graph.py %DATA_FILENAME% %GRAPH_FILENAME%