SELECT Cliente.nome, pedido.idPedido, pedido.DataPedido, pedido.ValorTotalPedido
FROM Cliente JOIN pedido ON Cliente.idcliente = pedido.Cliente_idCliente
WHERE Cliente.TipoCliente_idTipoCliente = 1 AND pedido.ValorTotalPedido = 0;

SELECT cliente.nome, pedido.idPedido, pedido.DataPedido, Status.descricao, pedido.ValorTotalPedido
FROM cliente JOIN pedido ON cliente.idcliente = pedido.Cliente_idCliente
JOIN Status ON Status.idstatus = pedido.status_idstatus
WHERE Status.descricao = 'Aberto' AND cliente.TipoCliente_idTipoCliente = 1 AND pedido.ValorTotalPedido = 0;

SELECT cliente.nome, pedido.idPedido, pedido.DataPedido, Status.descricao, pedido.ValorTotalPedido, produto.QuantEstoque
FROM cliente JOIN pedido ON cliente.idcliente = pedido.Cliente_idCliente
JOIN Status ON Status.idstatus = pedido.status_idstatus
JOIN pedido_has_produto ON pedido_has_produto.pedido_idPedido = pedido.idPedido
JOIN produto ON produto.idProduto = pedido_has_produto.produto_idProduto
WHERE Status.descricao = 'Aberto' AND cliente.TipoCliente_idTipoCliente = 1 AND pedido.ValorTotalPedido = 0 AND produto.QuantEstoque > 0;
