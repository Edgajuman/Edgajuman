# Mantener el perfil

El perfil se publica desde `Edgajuman/Edgajuman`. Edita `README.md` para cambiar presentación, proyectos y enlaces. Los forks y proyectos históricos se identifican explícitamente.

El banner GIF y las cinco cubiertas SVG se generan con `scripts/generate_assets.py`; requiere Pillow. Son recursos originales de este perfil. El GIF dura seis segundos, se repite suavemente y tiene una alternativa SVG estática para movimiento reducido. La captura del editor enlaza al repositorio público de AK Screen.

```sh
python -m pip install -r requirements.txt
python scripts/generate_assets.py
```

Las tarjetas de actividad se actualizan semanalmente con **Actions → Refresh profile activity** y también admiten ejecución manual. El script consulta únicamente metadatos de repositorios públicos, excluye este perfil y genera variantes claras y oscuras. No necesita servicios de estadísticas externos ni secretos personalizados.

```sh
python scripts/update_activity.py
```

Los enlaces de descarga apuntan a Releases para seguir vigentes entre versiones. Para añadir proyectos, describe su estado real y conserva la atribución de los forks. Las licencias de los proyectos destacados son independientes de los recursos de este perfil.
