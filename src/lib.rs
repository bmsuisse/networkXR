mod accel;

use pyo3::prelude::*;

#[pymodule]
fn _accel(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<accel::IntGraphCore>()?;
    Ok(())
}
