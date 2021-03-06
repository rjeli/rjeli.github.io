---
layout: post
title: 'Lab Notes: Inverse raytracing for localization with NeRF'
---

I was very impressed by this paper released a few days ago: [Representing Scenes as Neural Radiance Fields for View Synthesis][nerf], or NeRF for short. Check it out:

<video controls width="300" src="https://storage.googleapis.com/nerf_data/website_renders/redtoyota.mp4"></video>
<video controls width="300" src="https://storage.googleapis.com/nerf_data/website_renders/fern_200k_rgb.mp4"></video>

Sure, the reflections are cool, but check out the leaves on that fern! Above and beyond previous TSDF, octree or triangle-based neural renderers.

Essentially, you represent a scene as a network that predicts $$f(x,y,z) = (r,g,b,density)$$, and then train it by performing differentiable volumetric ray tracing on a set of images of the same scene with known poses. You can also feed in the viewing angle as $$f(x,y,z,\theta,\phi)$$ and get really nice specular reflections. They use an alpha-compositing render equation that's explained in detail in the paper. Here's the simplified code:

```
def get_rays(H, W, focal, pose):
    j, i = torch.meshgrid(torch.arange(H).float(), torch.arange(W).float())
    dirs = torch.stack([(i-W/2)/focal, -(j-H/2)/focal, -torch.ones_like(i)], -1)
    ray_origins = pose[:3,3]
    ray_directions = dirs @ pose[:3,:3]

def render_rays(model, ray_os, ray_ds, near, far, n_samples, add_noise=False):
    # sample points along rays
    z_vals = torch.linspace(near, far, steps=n_samples)
    if add_noise:
        z_vals += torch.rand_like(z_vals) * (far-near)/n_samples
    pts = rays_o + rays_d * z_vals
    
    # run model
    pts_flat = pts.view(-1, INPUT_SZ)
    pred = model(pts_flat).view(*(pts.shape[:-1] + (PRED_SZ,)))
    
    # densities and colors at points
    density = F.relu(pred[...,3])
    rgb = torch.sigmoid(pred[...,:3])
    
    # volumetric rendering
    dists = torch.cat([z_vals[...,1:] - z_vals[...,:-1], 1e10], -1)
    alpha = 1 - torch.exp(-density * dists)
    weights = alpha * torch.cumprod(1 - alpha + 1e-10, -1)
    
    rgb_img = (weights * rgb).sum(dim=-2)
    depth_img = (weights * z_vals).sum(dim=-1)
```

The real code, a quick port of the paper to PyTorch, and the code for rest of this post is in a notebook [here][code], and it's about the same number of lines, just with `broadcast`s, `expand`s and `view`s where needed.

The net's super simple, just 5 or 10 dense layers with relus, no batchnorm. The authors point out the parameters come out to ~5 Mb, smaller than any one of the uncompressed input images.

However, it's a bit annoying that we need exact poses for the input images. Ideally I can just feed in my vacation images and get out a 3d model. For starters, can we localize a new image into an existing scene? Here's what I have off the top of my head:

Render a set of images at randomly sampled poses, then do sparse keypoint matching in image space. You'd get real scaled 3d poses from this because the net outputs depth for free.

Sample an octree from the net and either do classic colmap-style photometric optimization or some crazy mono depth net to ICP pipeline. Honestly, the latter seems more likely to work, probably just for indoor scenes and jointly optimizing the predicted depth scale factor. Initially it seemed silly to spend all this time training a net to represent the scene and then sampling an octree from it anyways, but it probably makes sense to have both representations handy.

Run a particle filter over possible poses. The probability of a given pose is calculated by sampling $$N$$ pixels and using the MSE against net-sampled pixels. This is probably the least feasible solution, but I really like it for some reason. It would be prohibitively expensive for uniformly sampled particles, and not that great at refinement once you're in the general vicinity, so maybe good for medium-range relocalization. It may be possible to do smart things like edge sampling and then dense alignment in image space for fast refinement.

None of the above options take advantage of the fact that gradients flow all the way back into the pose. If you freeze the net and train the pose, you're using the gradient along the net's scene representation manifold, which you would think is pretty non-convex. However, it works surprisingly okay in my experiments:

<script type="text/javascript">
function play(shouldPlay) {
    document.querySelectorAll('.playable').forEach(el => {
        shouldPlay ? el.play() : el.pause();
    });
}
</script>
<button onclick="play(true)">Play all</button>
<button onclick="play(false)">Pause all</button>
(Left is render, right is error)
{% for i in (0..11) %}
<video controls loop class="playable" width="300" src="/assets/localize{{ i }}.mp4"></video>
{% endfor %}

[nerf]: http://www.matthewtancik.com/nerf
[code]: https://github.com/rjeli/nerf-experiments/blob/master/localization.ipynb

