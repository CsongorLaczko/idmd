from idmd import (
    ColumnManipulatorUI,
    DataApp,
    DataExporterUI,
    DataPreview,
    DataStats,
    DataVisualizerUI,
    FileUploaderUI,
    ReplaceUI,
    ReportUI,
)

app = DataApp()
(
    app.set_column_name(0, "Description | Manipulation")
    .add_component(FileUploaderUI())
    .add_component(DataPreview())
    .add_component(DataStats())
    .add_component(ReplaceUI())
    .add_component(ColumnManipulatorUI())
    .add_component(DataExporterUI())
    .add_component(ReportUI())
    .set_column_name(1, "Visualization | Export | Report")
    .add_component(DataVisualizerUI(position=1))
)
app.run()
