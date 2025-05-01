Usage
=====

To use our package, create a python script the following way. First, import all the modules (features) you would like to add to you dashboard.

.. code-block:: python

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

Once imported, these modules can be used as components for your dashboard. Create a 'DataApp' class and add the desired components, like this:

.. code-block:: python

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

After this class has been created, call our run function on the class:

.. code-block:: python

  app.run()

Finally, run this python script with streamlit in your command line:

.. code-block:: console

  streamlit run file_name.py
