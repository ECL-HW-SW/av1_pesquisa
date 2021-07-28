import numpy as np

def av1_nn_output_prec_reduce(output, num_output):
  prec_bits = 11
  prec = 1 << prec_bits
  inv_prec = (float(1.0 / prec))
  for i in range(num_output):
    output[i] = ((int(output[i] * prec + 0.5))) * inv_prec
    #print("\n\noutput: ", output)
  return(output[i])

def av1_nn_predict_c(input_nodes,j,nn_config):

  #print("\n\ninput: ", input_nodes)

  singl = nn_config.instance()

  reduce_prec = 1

  num_input_nodes = nn_config.num_inputs
  buf_index = 0

  # weights = nn_config.weights
  # bias = nn_config.bias

  num_layers = nn_config.num_hidden_layers

  assert num_layers <= nn_config.NN_MAX_HIDDEN_LAYERS
  for layer in range (num_layers):
    singl.layer_weights = nn_config.weights[j]
    singl.layer_bias = nn_config.bias[j]
    singl.output_nodes = nn_config.buf[buf_index]

    num_output_nodes = nn_config.num_hidden_nodes[j][layer]

    assert num_output_nodes < nn_config.NN_MAX_NODES_PER_LAYER
    k=-1
    for node in range(int(num_output_nodes)):
      val = singl.layer_bias[node];

      for i in range (num_input_nodes):
        k=+1
        # print(layer_weights[node * num_input_nodes + i])
        val += singl.layer_weights[k] * input_nodes[i]

      val = max(val, 0)

      singl.output_nodes[node] = val

    num_input_nodes = num_output_nodes
    input_nodes = singl.output_nodes
    buf_index = 1 - buf_index

  singl.layer_weights = nn_config.weights[num_layers]
  singl.layer_bias = nn_config.bias[num_layers]

  nn_config.output

  k=-1
  for node in range (nn_config.num_outputs):
    val = singl.layer_bias[node]

    for i in range (num_input_nodes):
      k=+1
      val += singl.layer_weights[k] * input_nodes[i]
    nn_config.output[node] = val

  if (reduce_prec):
    out = av1_nn_output_prec_reduce(nn_config.output, nn_config.num_outputs);
  return(out)

# if __name__ == '__main__':
#   av1_nn_predict_c(input_nodes,j)
