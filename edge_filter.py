def edge_filter(global_chain,cutter):
    for i in global_chain:
        if len(i) < cutter:
            global_chain.remove(i)
    return global_chain