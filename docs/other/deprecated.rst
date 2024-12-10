PyNiryo2 Deprecation Notice
===========================

.. contents::
   :local:


The decision to deprecate this project was made after the following assessment: PyNiryo and PyNiryo2 are very similar in terms of what they offer to users. Having two APIs creates unnecessary confusion and doesn't make sense. Moreover, maintaining two distinct projects reduces the time available to develop new features.

We had to choose between PyNiryo and PyNiryo2, and we chose to keep the former. Below are the reasons for this decision:

Reasons for deprecation
-----------------------

More reliable underlying protocols
**********************************

PyNiryo2 uses the `rosbridge_suite <http://wiki.ros.org/rosbridge_suite>`_ under the hood, which has certain limitations and does not fully meet our reliability requirements. We stopped using it in our GUI application, NiryoStudio, and it was natural to discontinue its use in our Python API as well.

PyNiryo, on the other hand, uses a custom protocol over TCP, which is more reliable and designed specifically for our needs. This protocol is also ROS-agnostic, providing an abstraction layer between the robot's internals and the user. This design ensures the interface is not tied to our private implementations.

Larger community
****************

PyNiryo has a bigger user community and is more widely adopted than PyNiryo2. This means deprecating PyNiryo2 minimizes the overall impact on our user base. Additionally, it shows that PyNiryo aligns closer with the needs of the majority of our users.

More mature codebase
*********************

PyNiryo has been available for a longer time than PyNiryo2 and has undergone more releases. This makes PyNiryo a more mature and reliable solution, with fewer bugs compared to PyNiryo2.

Downsides of PyNiryo2's deprecation
-----------------------------------

We recognize that PyNiryo2 offers some features not currently available in PyNiryo. Rest assured, we are actively working to add these features to PyNiryo. Our goal is to ensure PyNiryo achieves the same level of functionality as PyNiryo2 before its deprecation.

Another inherent downside is that users will need to migrate their code from PyNiryo2 to PyNiryo. However, while we understand that migrating code may involve effort, we are confident that the long-term benefits of PyNiryo will make this transition worthwhile. Since PyNiryo and PyNiryo2 have very similar interfaces, the migration process should be straightforward.

What's next?
------------
We will officially deprecate PyNiryo2 on June 1, 2025, giving users approximately six months to migrate to PyNiryo. After this date, PyNiryo2 will no longer be maintained or receive updates. Starting immediately, PyNiryo2 will only receive critical bug fixes and no new features.