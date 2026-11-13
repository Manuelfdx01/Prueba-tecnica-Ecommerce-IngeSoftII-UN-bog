import { useMemo, useState } from "react";

export function useCart() {
  const [items, setItems] = useState([]);

  const count = useMemo(
    () => items.reduce((total, item) => total + item.quantity, 0),
    [items],
  );

  const total = useMemo(
    () => items.reduce(
      (amount, item) => amount + Number(item.price) * item.quantity,
      0,
    ),
    [items],
  );

  function add(product) {
    if (!product.stock) {
      return { ok: false, message: "Este producto está agotado" };
    }

    const existing = items.find((item) => item.id === product.id);
    if (existing && existing.quantity >= product.stock) {
      return { ok: false, message: "No hay más unidades disponibles" };
    }

    setItems((current) => {
      const currentItem = current.find((item) => item.id === product.id);
      return currentItem
        ? current.map((item) =>
            item.id === product.id
              ? { ...item, quantity: item.quantity + 1 }
              : item,
          )
        : [...current, { ...product, quantity: 1 }];
    });

    return { ok: true, message: "Producto agregado al carrito" };
  }

  function changeQuantity(productId, difference) {
    setItems((current) =>
      current.map((item) =>
        item.id === productId
          ? {
              ...item,
              quantity: Math.max(
                1,
                Math.min(item.stock, item.quantity + difference),
              ),
            }
          : item,
      ),
    );
  }

  function remove(productId) {
    setItems((current) =>
      current.filter((item) => item.id !== productId),
    );
  }

  function clear() {
    setItems([]);
  }

  return {
    items,
    count,
    total,
    add,
    changeQuantity,
    remove,
    clear,
  };
}
