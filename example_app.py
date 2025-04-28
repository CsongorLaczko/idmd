from idmd import (
    ColumnManipulator,
    DataApp,
    DataExporter,
    DataStats,
    DataVisualizer,
    FileUploader,
)

app = DataApp(title="Advanced Data Explorer")
(
    app.add_component(FileUploader())
     .add_component(DataStats())
     .add_component(ColumnManipulator())
     .add_component(DataVisualizer())
     .add_component(DataExporter())
)
app.run()