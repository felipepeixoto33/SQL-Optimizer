Select cliente.nome, pedido.idPedido, pedido.DataPedido, pedido.ValorTotalPedido
from Cliente Join pedido on cliente.idcliente = pedido.Cliente_idCliente
where cliente.TipoCliente_idTipoCliente = 1 and pedido.ValorTotalPedido = 0;


Select cliente.nome, pedido.idPedido, pedido.DataPedido, Status.descricao, pedido.ValorTotalPedido
from Cliente Join pedido on cliente.idcliente = pedido.Cliente_idCliente
Join Status on Status.idstatus = Pedido.status_idstatus
where Status.descricao = 'Aberto' and cliente.TipoCliente_idTipoCliente = 1 and pedido.ValorTotalPedido = 0;

Select cliente.nome, pedido.idPedido, pedido.DataPedido, Status.descricao, pedido.ValorTotalPedido, produto.QuantEstoque
from Cliente Join pedido on cliente.idcliente = pedido.Cliente_idCliente
Join Status on Status.idstatus = Pedido.status_idstatus
Join pedido_has_produto on pedido.idPedido = pedido_has_produto.Pedido_idPedido
Join produto on produto.idProduto = pedido_has_produto.Produto_idProduto
where Status.descricao = 'Aberto' and cliente.TipoCliente_idTipoCliente = 1 and pedido.ValorTotalPedido = 0 and produto.QuantEstoque > 0;