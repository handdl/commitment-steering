def make_hook(store, layer_idx):
    def hook(module, inp, out):
        store[layer_idx].append(out[:, -1, :].detach().cpu())

    return hook


def make_delta_hook(delta, alpha):
    def hook(module, inp, out):
        if alpha == 0:
            return out
        if isinstance(out, tuple):
            h = out[0]
            h = h + alpha * delta.to(device=h.device, dtype=h.dtype)
            return (h,) + out[1:]
        else:
            return out + alpha * delta.to(device=out.device, dtype=out.dtype)

    return hook
